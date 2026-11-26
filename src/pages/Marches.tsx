import { useEffect, useState } from "react";
import { supabase } from "../lib/supabase";

type Marche = { id: string; entreprise: string; montant_ht: number; cout_interne: number; marge: number };

export default function Marches() {
  const [marches, setMarches] = useState<Marche[]>([]);
  useEffect(() => {
    supabase.from("marches").select("*").then(({ data }) => setMarches(data ?? []));
  }, []);
  return (
    <table>
      <tbody>
        {marches.map((m) => (
          <tr key={m.id}>
            <td>{m.entreprise}</td>
            <td>{m.montant_ht}</td>
            <td>{m.marge}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
