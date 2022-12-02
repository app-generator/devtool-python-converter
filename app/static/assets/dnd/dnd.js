// html elements
const fileInput = document.querySelector("#file_upload");
const dropAreaBorder = document.querySelector("#custom-file-uploader");
const dropAreaLabel = document.querySelector("#file-upload-label");
const selectContainer = document.querySelector("#select-container");
const selectOutput = document.querySelector("#select-output");
const generateContainer = document.querySelector("#generate-container");
const generateButton = document.querySelector("#generate");
const copyButtons = document.querySelectorAll(".copy-button");
const selectedFlaskRow = document.querySelector("#selected-row-1");
const selectedDjangoRow = document.querySelector("#selected-row-2");
const editSelect1 = document.querySelector("#select-1");
const editContainer1 = document.querySelector("#edit-container-1");
const applyChange1 = document.querySelector("#apply-change-1");
const editSelect2 = document.querySelector("#select-2");
const editContainer2 = document.querySelector("#edit-container-2");
const applyChange2 = document.querySelector("#apply-change-2");
const validate1 = document.querySelector("#validate-1");
const validate2 = document.querySelector("#validate-2");
const flaskOutput = document.querySelector("#output-1");
const djangoOutput = document.querySelector("#output-2");

let file = null;

const UPLOAD_STATE = {
  drag: "drag",
  dragLeave: "dragLeave",
  success: "success",
  error: "error",
};

const VALID_EXTENSIONS = ["yaml", "json", "pkl", "csv"];
const FLASK_DJANGO = ["Flask", "Django", "Flask & Django"];
const IDK_THE_NAME = ["Model", "DataTable", "Charts", "Export"];
const FLASK_FIELDS = {
  selectType: "select type",
  boolean: "db.Column(db.Boolean)\n",
  integer: "db.Column(db.Integer)\n",
  string: "db.Column(db.String())\n",
  number: "db.Column(db.Float)\n",
  Text: "db.Column(db.Text)\n",
  DateTime: "db.Column(db.DateTime)\n",
  Boolean: "db.Column(db.Boolean)\n",
  PickleType: "db.Column(db.PickleType)\n",
  LargeBinary: "db.Column(db.LargeBinary)\n",
  Integer: "db.Column(db.Integer)\n",
  Float: "db.Column(db.Float)\n",
  String: "db.Column(db.String())\n",
};

const DJANGO_FIELDS = {
  selectType: "select type",
  boolean: "models.BooleanField()\n",
  integer: "models.IntegerField()\n",
  string: "models.CharField()\n",
  number: "models.FloatField()\n",
  UUIDField: "model.UUIDField()\n",
  URLField: "model.URLField()\n",
  TimeField: "model.TimeField()\n",
  TextField: "model.TextField()\n",
  SmallIntegerField: "model.SmallIntegerField()\n",
  SmallAutoField: "model.SmallAutoField()\n",
  SlugField: "model.SlugField()\n",
  PositiveSmallIntegerField: "model.PositiveSmallIntegerField()\n",
  PositiveIntegerField: "model.PositiveIntegerField()\n",
  PositiveBigIntegerField: "model.PositiveBigIntegerField()\n",
  JSONField: "model.JSONField()\n",
  IntegerField: "model.IntegerField()\n",
  ImageField: "model.ImageField()\n",
  GenericIPAddressField: "model.GenericIPAddressField()\n",
  FloatField: "model.FloatField()\n",
  FilePathField: "model.FilePathField()\n",
  FileField: "model.FileField()\n",
  EmailField: "model.EmailField()\n",
  DurationField: "model.DurationField()\n",
  DecimalField: "model.DecimalField()\n",
  DateTimeField: "model.DateTimeField()\n",
  DateField: "model.DateField()\n",
  CharField: "model.CharField()\n",
  BooleanField: "model.BooleanField()\n",
  BinaryField: "model.BinaryField()\n",
  BigIntegerField: "model.BigIntegerField()\n",
  BigAutoField: "model.BigAutoField()\n",
};

const preventDefaults = (event) => {
  event.preventDefault();
  event.stopPropagation();
};

["drop", "dragenter", "dragover", "dragleave"].forEach((ev) => {
  dropAreaBorder.addEventListener(ev, preventDefaults);
});

["dragenter", "dragover"].forEach((ev) => {
  dropAreaBorder.addEventListener(ev, () => {
    dropAreaBorder.classList.remove("error-border", "success-border");
    dropAreaLabel.classList.remove("error-label", "success-label");
    dropAreaBorder.classList.add("highlight-border");
    dropAreaLabel.classList.add("highlight-label");
    dropAreaLabel.innerHTML = getDropAreaLabelText(UPLOAD_STATE.drag);
  });
});

["dragleave", "drop"].forEach((ev) => {
  dropAreaBorder.addEventListener(ev, () => {
    dropAreaBorder.classList.remove("highlight-border");
    dropAreaLabel.classList.remove("highlight-label");
  });
});

["dragleave"].forEach((ev) => {
  dropAreaBorder.addEventListener(ev, () => {
    dropAreaLabel.innerHTML = getDropAreaLabelText(UPLOAD_STATE.dragLeave);
  });
});

const getDropAreaLabelText = (state, ext, fileName) => {
  switch (state) {
    case UPLOAD_STATE.success:
      return `${fileName} uploaded successfully.`;
    case UPLOAD_STATE.error:
      return `${ext} is not a valid file extension.`;
    case UPLOAD_STATE.drag:
      return "drop it like it's hot.";
    case UPLOAD_STATE.dragLeave:
      return "drop your file here.";
  }
};

const addOption = (node, value) => {
  const optionNode = document.createElement("option");
  optionNode.innerHTML = value;
  optionNode.value = value;
  node.appendChild(optionNode);
};

const resetOptions = () => {
  const children = [...selectOutput.children];
  children.forEach((child) => selectOutput.removeChild(child));
  addOption(selectOutput, "select output");
};

const handleValidDrop = (fileName, fileExtension) => {
  dropAreaBorder.classList.remove("highlight-border", "error-border");
  dropAreaLabel.classList.remove("highlight-label", "error-label");
  dropAreaBorder.classList.add("success-border");
  dropAreaLabel.classList.add("success-label");
  dropAreaLabel.innerHTML = getDropAreaLabelText(
    UPLOAD_STATE.success,
    undefined,
    fileName
  );
  if (fileExtension === "pkl" || fileExtension === "csv") {
    selectContainer.classList.remove("hidden");
    generateContainer.classList.add("hidden");
    IDK_THE_NAME.forEach((option) => {
      addOption(selectOutput, option);
    });
  } else if (fileExtension === "json" || fileExtension === "yaml") {
    selectContainer.classList.remove("hidden");
    generateContainer.classList.add("hidden");
    FLASK_DJANGO.forEach((item) => addOption(selectOutput, item));
  } else {
    generateContainer.classList.remove("hidden");
    selectContainer.classList.add("hidden");
  }
};

const handleInvalidDrop = (fileExtension) => {
  dropAreaBorder.classList.remove("highlight-border", "success-border");
  dropAreaLabel.classList.remove("highlight-label", "success-label");
  dropAreaBorder.classList.add("error-border");
  dropAreaLabel.classList.add("error-label");
  dropAreaLabel.innerHTML = getDropAreaLabelText(
    UPLOAD_STATE.error,
    fileExtension
  );
  selectContainer.classList.add("hidden");
  generateContainer.classList.add("hidden");
};

const dropZoneDropHandler = (e) => {
  // console.log(e.dataTransfer.getData("URL"));
  file = e.dataTransfer.files[0];
  const fileName = file.name;
  const splittedFileName = fileName.split(".");
  const fileExtension =
    splittedFileName[splittedFileName.length - 1].toLocaleLowerCase();
  resetOptions();
  if (!VALID_EXTENSIONS.includes(fileExtension))
    handleInvalidDrop(fileExtension);
  else handleValidDrop(fileName, fileExtension);
};

const handleSelectOutput = (e) => {
  if (e.target.value !== "select output")
    generateContainer.classList.remove("hidden");
  else generateContainer.classList.add("hidden");
};

const handleExcludes = (res, exclude) => {
  for (const iterator of exclude) {
    if (res.includes(iterator)) {
      return false;
    }
  }
  return true;
};

const addTypesToSelect = (type, parent) => {
  const elem = parent.querySelectorAll(`select`);
  const object = type === "django" ? DJANGO_FIELDS : FLASK_FIELDS;
  for (const iterator of elem) {
    for (const key in object) {
      addOption(iterator, object[key]);
    }
  }
};
const detectType = (input, regex, exclude, type) => {
  let output = "";
  let counter = 1;
  for (const iterator of input.split("\n")) {
    const res = iterator.match(regex);
    let fOutput = "";
    if (res) {
      if (handleExcludes(res.input, exclude)) {
        const className = `select-${counter++}`;
        fOutput = iterator.replace(
          res[0],
          `<select class=${className}>  
              <option value=${res[0]}>${res[0]}</option>
            </select>`
        );
      } else {
        fOutput = iterator;
      }
    } else {
      fOutput = iterator;
    }
    output += fOutput + "\n";
  }
  return output;
};

let counter = 1;
let selectedRow_flask = null;
let selectedRow_django = null;
const handleApplyChange = (event) => {
  const type = event.target.id.includes("1") ? "flask" : "django";
  if (type === "flask") {
    const newValue = editSelect1.value;
    if (newValue !== "select type") {
      const identifier = selectedRow_flask.innerHTML.split("=")[0] + "= ";
      selectedRow_flask.innerHTML = identifier + `${newValue}`;
      validate1.classList.remove("hidden");
    }
    editContainer1.classList.remove("flex");
    editContainer1.classList.add("hidden");
    selectedRow_flask = null;
  } else {
    const newValue = editSelect2.value;
    if (newValue !== "select type") {
      const identifier = selectedRow_django.innerHTML.split("=")[0] + "= ";
      selectedRow_django.innerHTML = identifier + `${newValue}`;
      validate2.classList.remove("hidden");
    }
    editContainer2.classList.remove("flex");
    editContainer2.classList.add("hidden");
    selectedRow_django = null;
  }
};
const handleTypeChange = (e, type) => {
  const content = e.target.innerHTML;
  let avoidables =
    content.trim().startsWith("ID") || content.trim().startsWith("class");
  if (type === "django" && !avoidables) {
    selectedDjangoRow.innerHTML = content;
    editContainer2.classList.remove("hidden");
    editContainer2.classList.add("flex");
    selectedRow_django = e.target;
  }
  if (type === "flask" && !avoidables) {
    selectedFlaskRow.innerHTML = content;
    editContainer1.classList.remove("hidden");
    editContainer1.classList.add("flex");
    selectedRow_flask = e.target;
  }
};
const handleTypeEventListeners = (type) => {
  for (let index = 1; index < counter; index++) {
    document
      .querySelector(`.div-${type}-${index}`)
      .addEventListener("click", (event) => handleTypeChange(event, type));
  }
};
const divivize = (str, type) => {
  let ans = "";
  for (const iterator of str.split("\n")) {
    const className = `div-${type}-${counter++}`;
    ans += `<div class=${className}>${iterator + "\n"}</div>`;
  }
  return ans;
};

const showFlaskDjangoOutput = (output) => {
  document.getElementById("output-wrapper-1").classList.add("hidden");
  document.getElementById("output-wrapper-2").classList.add("hidden");
  const { flask, django } = output;
  document.getElementById("output-container").classList.add("flex");
  if (flask) {
    counter = 1;
    document.getElementById("output-wrapper-1").classList.remove("hidden");
    const elem = document.querySelector(".output-1");
    // elem.innerHTML = flask["#codes$"];
    elem.innerHTML = divivize(flask["#codes$"], "flask");
    handleTypeEventListeners("flask");
    // elem.innerHTML = detectType(
    //   flask["#codes$"],
    //   /\(db..+/,
    //   ["db.Model"],
    //   "flask"
    // );
  }
  if (django) {
    counter = 1;
    document.getElementById("output-wrapper-2").classList.remove("hidden");
    const elem = document.querySelector(".output-2");
    // elem.innerHTML = django["#codes$"];
    elem.innerHTML = divivize(django["#codes$"], "django");
    handleTypeEventListeners("django");
    // elem.innerHTML = detectType(
    //   django["#codes$"],
    //   /models..+/,
    //   ["models.Model", "models.AutoField"],
    //   "django"
    // );
    // addTypesToSelect("django", elem);
  }
};

const sendData = async (body, url, method) => {
  const request = await fetch(url, {
    method,
    body,
  });
  const result = await request.json().then((error) => error);
  showFlaskDjangoOutput(result);
};

const sendDataWrapper = () => {
  const output = document.querySelector("#select-output").value;
  if (FLASK_DJANGO.includes(output) || IDK_THE_NAME.includes(output)) {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("type", "file");
    formData.append("output", output);
    const url = "http://127.0.0.1:5000/";
    const method = "POST";
    sendData(formData, url, method);
  } else {
  }
};

const copyToClipboard = (text) => {
  navigator.clipboard.writeText(text);
};

const findOutputText = (targetElement) => {
  const target = targetElement === "copy-button-1" ? "#output-1" : "#output-2";
  const element = document.querySelector(target);
  return element.innerText;
};

const alertCopy = (node) => {
  node.innerHTML = "copied";
  setTimeout(() => {
    node.innerHTML = "copy";
  }, 2000);
};

const handleOutputCopy = (event) => {
  const outputText = findOutputText(event.currentTarget.id);
  copyToClipboard(outputText);
  alertCopy(event.currentTarget.querySelector("#copy-state"));
};

const updateData = async (body, url, method) => {
  const result = await fetch(url, {
    method,
    body,
  });
  const response = await result.json().catch((error) => error);
  console.log(response);
};

const updateDataWrapper = (e) => {
  const djangoUpdated = djangoOutput.textContent;
  const flaskUpdated = flaskOutput.textContent;
  const type = "update";
  const url = "http://127.0.0.1:5000/";
  const method = "POST";
  const formData = new FormData();
  const updatedValues = {
    django: djangoUpdated,
    flask: flaskUpdated,
  };
  formData.append("type", type);
  formData.append("update", updatedValues);
  updateData(formData, url, method);
  e.target.classList.add("hidden");
};

dropAreaBorder.addEventListener("drop", dropZoneDropHandler);
selectOutput.addEventListener("change", handleSelectOutput);
generateButton.addEventListener("click", sendDataWrapper);
copyButtons.forEach((button) =>
  button.addEventListener("click", handleOutputCopy)
);
Object.values(FLASK_FIELDS).forEach((value) => {
  addOption(editSelect1, value);
});
Object.values(DJANGO_FIELDS).forEach((value) => {
  addOption(editSelect2, value);
});
[applyChange1, applyChange2].forEach((button) =>
  button.addEventListener("click", handleApplyChange)
);
[validate1, validate2].forEach((button) =>
  button.addEventListener("click", updateDataWrapper)
);
