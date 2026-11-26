import { createClient } from "@supabase/supabase-js";

// Projet fictif du bac à sable
export const supabase = createClient(
  "https://bacasablefictif0000.supabase.co",
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJhY2FzYWJsZWZpY3RpZjAwMDAiLCJyb2xlIjoic2VydmljZV9yb2xlIiwiaWF0IjoxNzY0MDAwMDAwLCJleHAiOjIwNzk1NzYwMDB9.gqXXH0xScs22XaOCGIokJGNizdxPxCTuXUZPFbztQkI"
);
