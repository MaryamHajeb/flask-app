const api = "/api/students";
let students = [];
const $ = (selector) => document.querySelector(selector);
const body = $("#students-body");
const notice = $("#notice");
const dialog = $("#student-dialog");
const form = $("#student-form");

function showNotice(message, error = false) {
  notice.textContent = message;
  notice.className = `notice${error ? " error" : ""}`;
  notice.hidden = false;
  window.clearTimeout(showNotice.timer);
  showNotice.timer = window.setTimeout(() => { notice.hidden = true; }, 4200);
}

function escapeText(value) {
  const element = document.createElement("span");
  element.textContent = value;
  return element.innerHTML;
}

function render() {
  const term = $("#search-input").value.trim().toLowerCase();
  const visible = students.filter((student) => [student.name, student.email, student.department].some((value) => value.toLowerCase().includes(term)));
  $("#student-count").textContent = students.length;
  body.innerHTML = visible.map((student) => `<tr>
    <td><span class="student-name">${escapeText(student.name)}</span><span class="student-email">${escapeText(student.email)}</span></td>
    <td><span class="tag">${escapeText(student.department)}</span></td><td><span class="id">#${student.id}</span></td>
    <td class="row-actions"><button class="text-button" data-edit="${student.id}">Edit</button><button class="text-button delete" data-delete="${student.id}">Delete</button></td>
  </tr>`).join("");
  $("#empty").hidden = students.length !== 0 || term !== "";
  $("#loading").hidden = true;
}

async function loadStudents() {
  $("#loading").hidden = false;
  try {
    const response = await fetch(api);
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error?.message || "Could not load students.");
    students = payload.data;
    render();
  } catch (error) {
    $("#loading").hidden = true;
    showNotice(error.message, true);
  }
}

function openForm(student = null) {
  form.reset(); $("#form-error").hidden = true;
  $("#student-id").value = student?.id || "";
  $("#dialog-title").textContent = student ? "Edit student" : "Add student";
  $("#dialog-kicker").textContent = student ? "UPDATE RECORD" : "NEW RECORD";
  $("#submit-student").textContent = student ? "Save changes" : "Save student";
  if (student) ["name", "email", "department"].forEach((field) => { $(`#${field}`).value = student[field]; });
  dialog.showModal(); $("#name").focus();
}

async function saveStudent(event) {
  event.preventDefault();
  const id = $("#student-id").value;
  const data = Object.fromEntries(new FormData(form));
  const errorBox = $("#form-error");
  try {
    const response = await fetch(id ? `${api}/${id}` : api, { method: id ? "PUT" : "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) });
    const payload = await response.json();
    if (!response.ok) { const details = payload.error?.details; throw new Error(details ? Object.values(details).join(" ") : (payload.error?.message || "Could not save student.")); }
    dialog.close(); showNotice(id ? "Student updated." : "Student added."); await loadStudents();
  } catch (error) { errorBox.textContent = error.message; errorBox.hidden = false; }
}

body.addEventListener("click", async (event) => {
  const id = Number(event.target.dataset.edit || event.target.dataset.delete);
  if (!id) return;
  const student = students.find((item) => item.id === id);
  if (event.target.dataset.edit) openForm(student);
  if (event.target.dataset.delete && window.confirm(`Delete ${student.name}?`)) {
    try { const response = await fetch(`${api}/${id}`, { method: "DELETE" }); if (!response.ok) throw new Error("Could not delete student."); showNotice("Student deleted."); await loadStudents(); } catch (error) { showNotice(error.message, true); }
  }
});

$("#open-create").addEventListener("click", () => openForm());
document.querySelector("[data-open-create]").addEventListener("click", () => openForm());
$("#close-dialog").addEventListener("click", () => dialog.close());
$("#cancel-dialog").addEventListener("click", () => dialog.close());
$("#refresh").addEventListener("click", loadStudents);
$("#search-input").addEventListener("input", render);
form.addEventListener("submit", saveStudent);
loadStudents();
