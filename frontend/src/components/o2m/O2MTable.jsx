import { Table } from "react-bootstrap";
import O2MRow from "./O2MRow";
import O2MNewRow from "./O2MNewRow";
import { useO2M } from "./O2MProvider";

export default function O2MTable({ items }) {

  const {columns} = useO2M();
  return (
    <Table bordered size="sm">
      <thead>
        <tr>
          {columns.map(c => (
            <th key={c.field}>{c.label}</th>
          ))}
          <th />
        </tr>
      </thead>

      <tbody>
        {items.map(item => (
          <O2MRow key={item.id} item={item} />
        ))}
        <O2MNewRow />
      </tbody>
    </Table>
  );
}

