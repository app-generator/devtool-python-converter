// html elements
const fileInput = document.querySelector("#file_upload");
const dropAreaBorder = document.querySelector("#custom-file-uploader");
const dropAreaLabel = document.querySelector("#file-upload-label");
const selectContainer = document.querySelector("#select-container");
const selectOutput = document.querySelector("#select-output");
const outputContainer = document.querySelector("#output-container");
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
// const validate1 = document.querySelector("#validate-1");
// const validate2 = document.querySelector("#validate-2");
const flaskOutput = document.querySelector("#output-1");
const djangoOutput = document.querySelector("#output-2");
const chartOutput = document.querySelector("#chart");
const chartFlex = document.querySelector("#chart-flex");
const chartType = document.querySelector("#select-chart-type");
const chartX = document.querySelector("#select-x");
const chartY = document.querySelector("#select-y");
const chartOptionsContainer = document.querySelector(
  "#flex-select-chart-options"
);

// constants
let file = null;
let myChart = null;
let chartInfo = null;

const UPLOAD_STATE = {
  drag: "drag",
  dragLeave: "dragLeave",
  success: "success",
  error: "error",
};

const VALID_EXTENSIONS = ["yaml", "json", "pkl", "csv"];

const OPENAPI_OUTPUT = ["Flask", "Django", "Flask & Django"];

const CSV_OUTPUT = ["Model", "DataTable", "Charts"];

const CHART_TYPES = [
  "line",
  "bar",
  "radar",
  "doughnut",
  "pie",
  "polarArea",
  "bubble",
  "scatter",
];

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

let COUNTER = 1;
let SELECTED_ROW_FLASK = null;
let SELECTED_ROW_DJANGO = null;

// prevents default behaviours when dropping a file
const preventDefaults = (event) => {
  event.preventDefault();
  event.stopPropagation();
};

// handles dragEnter and dragOver events
const draggingHandler = () => {
  dropAreaBorder.classList.remove("error-border", "success-border");
  dropAreaLabel.classList.remove("error-label", "success-label");
  dropAreaBorder.classList.add("highlight-border");
  dropAreaLabel.classList.add("highlight-label");
  dropAreaLabel.innerHTML = getDropAreaLabelText(UPLOAD_STATE.drag);
};

// handles dragLeave and drop events
const dragStopHandler = () => {
  dropAreaBorder.classList.remove("highlight-border");
  dropAreaLabel.classList.remove("highlight-label");
};

// handles dragLeave event
const dragEndHandler = () => {
  dropAreaLabel.innerHTML = getDropAreaLabelText(UPLOAD_STATE.dragLeave);
};

// determines drop area label depending on the upload state
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

// adds option tag with value to the select tag(node)
const addOption = (node, value) => {
  const optionNode = document.createElement("option");
  optionNode.innerHTML = value;
  optionNode.value = value;
  node.appendChild(optionNode);
};

// resets the options in a given node ans adds a default option
const resetOptions = (node, defaultVal) => {
  const children = [...node.children];
  children.forEach((child) => node.removeChild(child));
  addOption(node, defaultVal);
};

// handles the case when the dropped file is valid
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
    CSV_OUTPUT.forEach((option) => {
      addOption(selectOutput, option);
    });
  } else if (fileExtension === "json" || fileExtension === "yaml") {
    selectContainer.classList.remove("hidden");
    generateContainer.classList.add("hidden");
    OPENAPI_OUTPUT.forEach((item) => addOption(selectOutput, item));
  } else {
    generateContainer.classList.remove("hidden");
    selectContainer.classList.add("hidden");
  }
};

// handles the case when the dropped file is not valid
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

// listens to all drop events on the determined div tag
const dropZoneDropHandler = (e) => {
  // console.log(e.dataTransfer.getData("URL"));
  file = e.dataTransfer.files[0];
  const fileName = file.name;
  const splittedFileName = fileName.split(".");
  const fileExtension =
    splittedFileName[splittedFileName.length - 1].toLocaleLowerCase();
  resetOptions(selectOutput, "select output");
  if (!VALID_EXTENSIONS.includes(fileExtension))
    handleInvalidDrop(fileExtension);
  else handleValidDrop(fileName, fileExtension);
};

const fillChartOptions = async () => {
  [chartType, chartX, chartY].forEach((node) => resetOptions(node, ""));
  const fileURL = URL.createObjectURL(file);
  chartInfo = await d3.csv(fileURL).then((res) => res);
  const columns = Object.keys(chartInfo[0]);
  columns.forEach((column) => {
    addOption(chartX, column);
    addOption(chartY, column);
  });
  CHART_TYPES.forEach((chart_type) => addOption(chartType, chart_type));
};

// listens to change event on the output selection tag
const handleSelectOutput = (e) => {
  const value = e.target.value;
  if (value === "select output") {
    generateContainer.classList.add("hidden");
    chartFlex.classList.add("hidden");
    chartFlex.classList.remove("flex");
  } else if (value === "Charts") {
    outputContainer.classList.remove("flex");
    outputContainer.classList.add("hidden");
    generateContainer.classList.remove("hidden");
    chartFlex.classList.remove("hidden");
    chartFlex.classList.add("flex");
    chartOptionsContainer.classList.remove("hidden");
    fillChartOptions();
  } else {
    outputContainer.classList.remove("hideen");
    generateContainer.classList.remove("hidden");
    chartFlex.classList.add("hidden");
    chartFlex.classList.remove("flex");
  }
};

// handles changing types for flask or django output models
const handleApplyChange = (event) => {
  const type = event.target.id.includes("1") ? "flask" : "django";
  if (type === "flask") {
    const newValue = editSelect1.value;
    if (newValue !== "select type") {
      const identifier = SELECTED_ROW_FLASK.innerHTML.split("=")[0] + "= ";
      SELECTED_ROW_FLASK.innerHTML = identifier + `${newValue}`;
      // validate1.classList.remove("hidden");
    }
    editContainer1.classList.remove("flex");
    editContainer1.classList.add("hidden");
    SELECTED_ROW_FLASK = null;
  } else {
    const newValue = editSelect2.value;
    if (newValue !== "select type") {
      const identifier = SELECTED_ROW_DJANGO.innerHTML.split("=")[0] + "= ";
      SELECTED_ROW_DJANGO.innerHTML = identifier + `${newValue}`;
      // validate2.classList.remove("hidden");
    }
    editContainer2.classList.remove("flex");
    editContainer2.classList.add("hidden");
    SELECTED_ROW_DJANGO = null;
  }
};

// listens to click events fired on each div node in the models output(django or flask)
const handleTypeChange = (e, type) => {
  const content = e.target.innerHTML;
  let avoidables =
    content.trim().startsWith("ID") || content.trim().startsWith("class");
  if (type === "django" && !avoidables) {
    selectedDjangoRow.innerHTML = content;
    editContainer2.classList.remove("hidden");
    editContainer2.classList.add("flex");
    SELECTED_ROW_DJANGO = e.target;
  }
  if (type === "flask" && !avoidables) {
    selectedFlaskRow.innerHTML = content;
    editContainer1.classList.remove("hidden");
    editContainer1.classList.add("flex");
    SELECTED_ROW_FLASK = e.target;
  }
};

// adds event listeners for click event to each div node in the models output(flask or django)
const handleTypeEventListeners = (type) => {
  for (let index = 1; index < COUNTER; index++) {
    document
      .querySelector(`.div-${type}-${index}`)
      .addEventListener("click", (event) => handleTypeChange(event, type));
  }
};

// wraps each line of model output inside a distinguished div
const divivize = (str, type) => {
  let ans = "";
  for (const iterator of str.split("\n")) {
    const className = `div-${type}-${COUNTER++}`;
    ans += `<div class=${className}>${iterator + "\n"}</div>`;
  }
  return ans;
};

// renders flask or django output
const showFlaskDjangoOutput = (output) => {
  document.getElementById("output-wrapper-1").classList.add("hidden");
  document.getElementById("output-wrapper-2").classList.add("hidden");
  const { flask, django } = output;
  document.getElementById("output-container").classList.add("flex");
  if (flask) {
    COUNTER = 1;
    document.getElementById("output-wrapper-1").classList.remove("hidden");
    const elem = document.querySelector(".output-1");
    elem.innerHTML = divivize(flask["#codes$"], "flask");
    handleTypeEventListeners("flask");
  }
  if (django) {
    COUNTER = 1;
    document.getElementById("output-wrapper-2").classList.remove("hidden");
    const elem = document.querySelector(".output-2");
    elem.innerHTML = divivize(django["#codes$"], "django");
    handleTypeEventListeners("django");
  }
};

// sends an http request to the server containing uploaded file to be converted to flask or django output
const sendFlaskDjangoData = async (body, url, method) => {
  const request = await fetch(url, {
    method,
    body,
  });
  const result = await request.json().catch((error) => error);
  showFlaskDjangoOutput(result);
};

// renders a data table
const showDataTableOutput = async (res) => {
  const htmlText = await res.text();
  var newHTML = document.open("text/html", "replace");
  newHTML.write(htmlText);
  newHTML.close();
};

// sends an http request to the server containing uploaded file and expects a html document for later renders
const sendDataTableData = async (body, url, method) => {
  await fetch(url, {
    method,
    body,
  }).then((res) => showDataTableOutput(res));
};

// shows chart data using chartjs
const showChartData = async (chartType, x, y) => {
  myChart?.destroy();
  const labels = [...new Set(chartInfo.map((item) => item[x].toString()))];
  const data = chartInfo.map((item) => item[y]);
  const label = y;
  myChart = new Chart(chartOutput, {
    type: chartType,
    data: {
      labels,
      datasets: [
        {
          label,
          data,
        },
      ],
    },
  });
};

// prepers the required data for post request using sendData function
const sendDataWrapper = () => {
  const output = document.querySelector("#select-output").value;
  if (OPENAPI_OUTPUT.includes(output) || output === "Model") {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("type", "file");
    formData.append("output", output);
    const url = "http://127.0.0.1:5000/";
    const method = "POST";
    sendFlaskDjangoData(formData, url, method);
  } else if (output === "DataTable") {
    const formData = new FormData();
    formData.append("file", file);
    const url = "http://127.0.0.1:5000/datatb";
    const method = "POST";
    sendDataTableData(formData, url, method);
  } else if (output === "Charts") {
    const chartArr = [chartType.value, chartX.value, chartY.value];
    if (!chartArr.includes("")) {
      showChartData(...chartArr);
    } else {
      generateButton.innerHTML = `<div style="font-size:0.8rem;">select chart options</div>`;
      setTimeout(() => {
        generateButton.innerHTML = "Generate";
      }, 2000);
    }
  }
};

// copies the given parameter to clipboard
const copyToClipboard = (text) => {
  navigator.clipboard.writeText(text);
};

// returns text content in the given node
const findOutputText = (targetElement) => {
  const target = targetElement === "copy-button-1" ? "#output-1" : "#output-2";
  const element = document.querySelector(target);
  return element.innerText;
};

// alerts the user when the text is copied
const alertCopy = (node) => {
  node.innerHTML = "copied";
  setTimeout(() => {
    node.innerHTML = "copy";
  }, 2000);
};

// listens to click events on the copy buttons
const handleOutputCopy = (event) => {
  const outputText = findOutputText(event.currentTarget.id);
  copyToClipboard(outputText);
  alertCopy(event.currentTarget.querySelector("#copy-state"));
};

// sends an http request to the server containing updated django and flask models to be validated
// const updateData = async (body, url, method) => {
//   const result = await fetch(url, {
//     method,
//     body,
//   });
//   const response = await result.json().catch((error) => error);
//   console.log(response);
// };

// prepers the required data for post request using updateData function
// const updateDataWrapper = (e) => {
//   const djangoUpdated = djangoOutput.textContent;
//   const flaskUpdated = flaskOutput.textContent;
//   const type = "update";
//   const url = "http://127.0.0.1:5000/";
//   const method = "POST";
//   const formData = new FormData();
//   const updatedValues = {
//     django: djangoUpdated,
//     flask: flaskUpdated,
//   };
//   formData.append("type", type);
//   formData.append("update", JSON.stringify(updatedValues));
//   updateData(formData, url, method);
//   e.target.classList.add("hidden");
// };

// adds event listeners to different nodes

["drop", "dragenter", "dragover", "dragleave"].forEach((ev) => {
  dropAreaBorder.addEventListener(ev, preventDefaults);
});

["dragenter", "dragover"].forEach((ev) => {
  dropAreaBorder.addEventListener(ev, draggingHandler);
});

["dragleave", "drop"].forEach((ev) => {
  dropAreaBorder.addEventListener(ev, dragStopHandler);
});

["dragleave"].forEach((ev) => {
  dropAreaBorder.addEventListener(ev, dragEndHandler);
});

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

// [validate1, validate2].forEach((button) =>
//   button.addEventListener("click", updateDataWrapper)
// );
