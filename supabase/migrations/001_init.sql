-- 001_init.sql

-- Extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- #############################################################################
-- ### Tables
-- #############################################################################

-- Users Table (references auth.users)
CREATE TABLE public.users (
    id UUID PRIMARY KEY REFERENCES auth.users(id),
    username TEXT UNIQUE,
    full_name TEXT,
    avatar_url TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
COMMENT ON TABLE public.users IS 'Profile information for users, extending auth.users.';

-- Modules Table
CREATE TABLE public.modules (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL UNIQUE,
    slug TEXT NOT NULL UNIQUE,
    description TEXT,
    created_by UUID REFERENCES public.users(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);
COMMENT ON TABLE public.modules IS 'Defines custom CRM modules like Leads, Contacts, etc.';

-- Entities Table
CREATE TABLE public.entities (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    module_id UUID NOT NULL REFERENCES public.modules(id) ON DELETE CASCADE,
    owner_id UUID REFERENCES public.users(id),
    custom_fields JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
COMMENT ON TABLE public.entities IS 'Stores records for each module with dynamic custom fields.';
CREATE INDEX idx_entities_module_id ON public.entities(module_id);
CREATE INDEX idx_entities_custom_fields_gin ON public.entities USING GIN (custom_fields);

-- Notes Table
CREATE TABLE public.notes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    entity_id UUID NOT NULL REFERENCES public.entities(id) ON DELETE CASCADE,
    user_id UUID REFERENCES public.users(id),
    content TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
COMMENT ON TABLE public.notes IS 'Notes linked to a specific module entity.';

-- Files Table
CREATE TABLE public.files (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    entity_id UUID NOT NULL REFERENCES public.entities(id) ON DELETE CASCADE,
    user_id UUID REFERENCES public.users(id),
    file_name TEXT NOT NULL,
    storage_path TEXT NOT NULL,
    file_type TEXT,
    size BIGINT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
COMMENT ON TABLE public.files IS 'File attachments linked to entities.';

-- Tasks Table
CREATE TABLE public.tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    entity_id UUID REFERENCES public.entities(id) ON DELETE CASCADE,
    assignee_id UUID REFERENCES public.users(id),
    title TEXT NOT NULL,
    description TEXT,
    due_date DATE,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMPTZ DEFAULT NOW()
);
COMMENT ON TABLE public.tasks IS 'Tasks associated with entities or users.';

-- Meetings Table
CREATE TABLE public.meetings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    entity_id UUID REFERENCES public.entities(id) ON DELETE CASCADE,
    organizer_id UUID REFERENCES public.users(id),
    title TEXT NOT NULL,
    description TEXT,
    start_time TIMESTAMPTZ NOT NULL,
    end_time TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
COMMENT ON TABLE public.meetings IS 'Meetings scheduled related to entities.';

-- Comments Table
CREATE TABLE public.comments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    entity_id UUID REFERENCES public.entities(id) ON DELETE CASCADE,
    user_id UUID REFERENCES public.users(id),
    content TEXT,
    parent_comment_id UUID REFERENCES public.comments(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
COMMENT ON TABLE public.comments IS 'Comments and replies on entities.';

-- Notifications Table
CREATE TABLE public.notifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    recipient_user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    related_entity_id UUID REFERENCES public.entities(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);
COMMENT ON TABLE public.notifications IS 'In-app notifications for users.';

-- Audit Logs Table
CREATE TABLE public.audit_logs (
    id BIGSERIAL PRIMARY KEY,
    table_name TEXT NOT NULL,
    record_id UUID NOT NULL,
    old_data JSONB,
    new_data JSONB,
    changed_by UUID REFERENCES public.users(id),
    changed_at TIMESTAMPTZ DEFAULT NOW()
);
COMMENT ON TABLE public.audit_logs IS 'Tracks all data modifications for auditing purposes.';

-- #############################################################################
-- ### Audit Trail Trigger
-- #############################################################################

CREATE OR REPLACE FUNCTION record_changes()
RETURNS TRIGGER AS $$
DECLARE
    record_id UUID;
BEGIN
    IF (TG_OP = 'INSERT' OR TG_OP = 'UPDATE') THEN
        record_id := NEW.id;
    ELSE
        record_id := OLD.id;
    END IF;

    INSERT INTO public.audit_logs (table_name, record_id, old_data, new_data, changed_by)
    VALUES (
        TG_TABLE_NAME,
        record_id,
        CASE WHEN TG_OP = 'UPDATE' OR TG_OP = 'DELETE' THEN to_jsonb(OLD) ELSE NULL END,
        CASE WHEN TG_OP = 'INSERT' OR TG_OP = 'UPDATE' THEN to_jsonb(NEW) ELSE NULL END,
        auth.uid()
    );

    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Apply trigger to tables
CREATE TRIGGER entities_audit_trigger
AFTER INSERT OR UPDATE OR DELETE ON public.entities
FOR EACH ROW EXECUTE FUNCTION record_changes();

CREATE TRIGGER notes_audit_trigger
AFTER INSERT OR UPDATE OR DELETE ON public.notes
FOR EACH ROW EXECUTE FUNCTION record_changes();

-- #############################################################################
-- ### Row Level Security (RLS)
-- #############################################################################

-- Enable RLS for all tables
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.modules ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.entities ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.notes ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.files ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.tasks ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.meetings ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.comments ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.notifications ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.audit_logs ENABLE ROW LEVEL SECURITY;

-- Policies: Users can see their own profile
CREATE POLICY "Allow users to view their own profile"
ON public.users FOR SELECT
USING (auth.uid() = id);

-- Policies: Any authenticated user can view modules
CREATE POLICY "Allow authenticated users to view modules"
ON public.modules FOR SELECT
USING (auth.role() = 'authenticated');

-- Policies: Users can view entities they own or are assigned to
CREATE POLICY "Allow users to view entities they own"
ON public.entities FOR SELECT
USING (auth.uid() = owner_id);

CREATE POLICY "Allow users to insert their own entities"
ON public.entities FOR INSERT
WITH CHECK (auth.uid() = owner_id);

CREATE POLICY "Allow users to update their own entities"
ON public.entities FOR UPDATE
USING (auth.uid() = owner_id);

-- Policies: Notes - users can access notes for entities they can access
CREATE POLICY "Allow full access to notes based on entity access"
ON public.notes FOR ALL
USING (
    EXISTS (
        SELECT 1
        FROM public.entities
        WHERE entities.id = notes.entity_id
    )
);

-- Policies: Files - users can access files for entities they can access
CREATE POLICY "Allow full access to files based on entity access"
ON public.files FOR ALL
USING (
    EXISTS (
        SELECT 1
        FROM public.entities
        WHERE entities.id = files.entity_id
    )
);

-- Policies: Tasks - users can manage tasks assigned to them or related to entities they own
CREATE POLICY "Allow users to manage their own tasks"
ON public.tasks FOR ALL
USING (auth.uid() = assignee_id OR EXISTS (
    SELECT 1
    FROM public.entities
    WHERE entities.id = tasks.entity_id AND entities.owner_id = auth.uid()
));

-- Policies: Meetings - users can manage meetings they organize or for entities they own
CREATE POLICY "Allow users to manage their own meetings"
ON public.meetings FOR ALL
USING (auth.uid() = organizer_id OR EXISTS (
    SELECT 1
    FROM public.entities
    WHERE entities.id = meetings.entity_id AND entities.owner_id = auth.uid()
));

-- Policies: Comments - users can manage comments on entities they can access
CREATE POLICY "Allow full access to comments based on entity access"
ON public.comments FOR ALL
USING (
    EXISTS (
        SELECT 1
        FROM public.entities
        WHERE entities.id = comments.entity_id
    )
);

-- Policies: Notifications - users can only access their own notifications
CREATE POLICY "Allow users to access their own notifications"
ON public.notifications FOR ALL
USING (auth.uid() = recipient_user_id);

-- Policies: Audit Logs - Admins or service roles only
CREATE POLICY "Allow service_role to access audit logs"
ON public.audit_logs FOR SELECT
USING (current_user = 'supabase_admin' OR auth.role() = 'service_role');
