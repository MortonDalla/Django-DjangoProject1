-- supabase/seed.sql

-- #############################################################################
-- ### Seed Users
-- ### Note: Replace with actual user UUIDs from your Supabase auth.users table
-- #############################################################################

-- Create 3 sample users in the public.users table
-- Make sure these UUIDs correspond to actual users in auth.users
-- You may need to create users in the Supabase dashboard and get their IDs
INSERT INTO public.users (id, username, full_name, avatar_url)
VALUES
    ('8a78c402-8a6a-4b0d-972a-3e5c9b74c2f8', 'crm_admin', 'Admin User', 'https://example.com/avatar1.png'),
    ('9b34a4d4-f7a8-4f8a-9f8a-9a9a9a9a9a9a', 'sales_rep1', 'Sales Rep One', 'https://example.com/avatar2.png'),
    ('a1b2c3d4-e5f6-7890-1234-567890abcdef', 'sales_rep2', 'Sales Rep Two', 'https://example.com/avatar3.png')
ON CONFLICT (id) DO NOTHING;

-- #############################################################################
-- ### Seed Modules
-- #############################################################################

-- Create 2 initial modules: Leads and Contacts
INSERT INTO public.modules (id, name, slug, description, created_by)
VALUES
    ('1b9d6bcd-bbfd-4b2d-9b5d-ab8dfbbd4bed', 'Leads', 'leads', 'Tracking potential customers.', '8a78c402-8a6a-4b0d-972a-3e5c9b74c2f8'),
    ('2c8e7acd-caec-4b7d-8b4d-bc9efccd5bef', 'Contacts', 'contacts', 'Managing customer contact information.', '8a78c402-8a6a-4b0d-972a-3e5c9b74c2f8')
ON CONFLICT (id) DO NOTHING;

-- #############################################################################
-- ### Seed Custom Fields (via Entities)
-- ### This demonstrates how custom fields are stored in the JSONB column.
-- ### The frontend would use a schema to render forms for these fields.
-- #############################################################################

-- Seed 6 sample entities for the 'Leads' module with custom fields
INSERT INTO public.entities (module_id, owner_id, custom_fields)
VALUES
    -- Lead 1
    ('1b9d6bcd-bbfd-4b2d-9b5d-ab8dfbbd4bed', '9b34a4d4-f7a8-4f8a-9f8a-9a9a9a9a9a9a',
    '{
        "lead_source": "Website",
        "status": "New",
        "estimated_value": 5000,
        "follow_up_date": "2024-08-15",
        "is_qualified": false,
        "priority": "High"
    }'),
    -- Lead 2
    ('1b9d6bcd-bbfd-4b2d-9b5d-ab8dfbbd4bed', '9b34a4d4-f7a8-4f8a-9f8a-9a9a9a9a9a9a',
    '{
        "lead_source": "Referral",
        "status": "Contacted",
        "estimated_value": 12000,
        "follow_up_date": "2024-08-20",
        "is_qualified": true,
        "priority": "Medium"
    }');

-- Seed 6 sample entities for the 'Contacts' module with custom fields
INSERT INTO public.entities (module_id, owner_id, custom_fields)
VALUES
    -- Contact 1
    ('2c8e7acd-caec-4b7d-8b4d-bc9efccd5bef', 'a1b2c3d4-e5f6-7890-1234-567890abcdef',
    '{
        "email": "customer1@example.com",
        "phone": "123-456-7890",
        "company": "ABC Corp",
        "last_contacted": "2024-07-20",
        "newsletter_subscribed": true,
        "department": "Sales"
    }'),
    -- Contact 2
    ('2c8e7acd-caec-4b7d-8b4d-bc9efccd5bef', 'a1b2c3d4-e5f6-7890-1234-567890abcdef',
    '{
        "email": "customer2@example.com",
        "phone": "098-765-4321",
        "company": "XYZ Inc",
        "last_contacted": "2024-07-25",
        "newsletter_subscribed": false,
        "department": "Support"
    }');

-- Note: The concept of "6 custom fields for each module" is implicitly defined
-- by the structure of the JSONB data. The application logic (and potentially
-- another table for attribute definitions) would enforce which fields are
-- available for each module in the UI. This seed file just provides examples.
