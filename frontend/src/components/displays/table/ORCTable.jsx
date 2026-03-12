import { useState, useMemo } from "react";
import { Table, Pagination } from "react-bootstrap";

export default function ORCTable({
  columns = [],
  data = [],
  size = "sm",
  pageSize = 10,
}) {
  const [page, setPage] = useState(1);

  const totalPages = Math.ceil(data.length / pageSize);

  const paginatedData = useMemo(() => {
    const start = (page - 1) * pageSize;
    return data.slice(start, start + pageSize);
  }, [data, page, pageSize]);

  const goToPage = (p) => {
    if (p < 1 || p > totalPages) return;
    setPage(p);
  };

  return (
    <>
      <Table bordered hover size={size}>
        <thead>
          <tr>
            {columns.map((col) => (
              <th
                key={col.field}
                style={{ width: col.width }}
                className={`text-${col.align || "start"}`}
              >
                {col.label}
              </th>
            ))}
          </tr>
        </thead>

        <tbody>
          {paginatedData.length === 0 ? (
            <tr>
              <td colSpan={columns.length} className="text-center text-muted">
                Sin datos
              </td>
            </tr>
          ) : (
            paginatedData.map((row, index) => (
              <tr key={row.id ?? index}>
                {columns.map((col) => (
                  <td
                    key={col.field}
                    className={`text-${col.align || "start"}`}
                  >
                    {col.render
                      ? col.render(row[col.field], row)
                      : row[col.field]}
                  </td>
                ))}
              </tr>
            ))
          )}
        </tbody>
      </Table>

      {totalPages > 1 && (
        <div className="d-flex justify-content-center mt-3">
          <Pagination>
            <Pagination.First onClick={() => goToPage(1)} />
            <Pagination.Prev onClick={() => goToPage(page - 1)} />

            {[...Array(totalPages)].map((_, i) => (
              <Pagination.Item
                key={i}
                active={page === i + 1}
                onClick={() => goToPage(i + 1)}
              >
                {i + 1}
              </Pagination.Item>
            ))}

            <Pagination.Next onClick={() => goToPage(page + 1)} />
            <Pagination.Last onClick={() => goToPage(totalPages)} />
          </Pagination>
        </div>
      )}
    </>
  );
}