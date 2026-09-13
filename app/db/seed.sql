INSERT INTO public.transactions (id, telegram_user_id, type, amount, category, description, transaction_date, created_at)
VALUES
    (gen_random_uuid(), 123456789, 'EXPENSE'::public.transaction_type, 50000.00, 'Transport', 'Ojek Online', NOW(), NOW()),
    (gen_random_uuid(), 123456789, 'INCOME'::public.transaction_type, 2000000.00, 'Gaji', 'Bonus Project', NOW(), NOW()),
    (gen_random_uuid(), 123456789, 'EXPENSE'::public.transaction_type, 125000.00, 'Belanja', 'Supermarket', NOW(), NOW());