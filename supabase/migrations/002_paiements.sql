-- Paiements fictifs rattachés aux marchés
create table public.paiements (
  id uuid primary key default gen_random_uuid(),
  marche_id uuid not null references public.marches(id) on delete cascade,
  montant numeric(12,2) not null,
  paye_le date not null default current_date,
  iban_beneficiaire text
);

create index paiements_marche_idx on public.paiements(marche_id);
