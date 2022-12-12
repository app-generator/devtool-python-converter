import { myData } from "../data/index.js";

// table
window.dataTable = new simpleDatatables.DataTable("table", {
  data: myData,
  perPageSelect: [10, 25, 50],
  perPage: 10,
  labels: {
    placeholder: "Search...",
    perPage: "{select} entries per page",
    noRows: "No entries to found",
    info: "Showing {start} to {end} of {rows} entries",
  },
  searchable: true,
});
