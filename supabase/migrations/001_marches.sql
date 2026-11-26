-- Marchés fictifs d'un chantier fictif
create table public.marches (
  id uuid primary key default gen_random_uuid(),
  entreprise text not null,
  montant_ht numeric(12,2) not null,
  taux_tva numeric(5,4) not null default 0.20,
  deja_regle numeric(12,2) not null default 0,
  created_by uuid not null default auth.uid()
);

alter table public.marches enable row level security;

create policy marches_proprietaire on public.marches
  for all using (created_by = auth.uid()) with check (created_by = auth.uid());
