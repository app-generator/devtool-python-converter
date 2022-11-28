const fileInput = document.querySelector("#file_upload");
const dropAreaBorder = document.querySelector("#custom-file-uploader");
const dropAreaLabel = document.querySelector("#file-upload-label");
const selectContainer = document.querySelector("#select-container");
const selectOutput = document.querySelector("#select-output");
const generateContainer = document.querySelector("#generate-container");
const generateButton = document.querySelector("#generate");

let data = null;

const UPLOAD_STATE = {
  drag: "drag",
  dragLeave: "dragLeave",
  success: "success",
  error: "error",
};

const VALID_EXTENSIONS = ["yaml", "json", "pkl", "csv"];

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

const addOption = (value) => {
  const optionNode = document.createElement("option");
  optionNode.innerHTML = value;
  optionNode.value = value;
  selectOutput.appendChild(optionNode);
};

const resetOptions = () => {
  const children = [...selectOutput.children];
  children.forEach((child) => selectOutput.removeChild(child));
  addOption("select output");
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
    ["Model", "DataTable", "Charts", "Export"].forEach((option) => {
      addOption(option);
    });
  } else if (fileExtension === "json" || fileExtension === "yaml") {
    selectContainer.classList.remove("hidden");
    generateContainer.classList.add("hidden");
    ["Flask", "Django", "Flask & Django"].forEach((option) => {
      addOption(option);
    });
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
  data = e.dataTransfer.files[0];
  const fileName = data.name;
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

const sendData = () => {
  const formData = new FormData();
  formData.append("file", data);
};

dropAreaBorder.addEventListener("drop", dropZoneDropHandler);
selectOutput.addEventListener("change", handleSelectOutput);
generateButton.addEventListener("click", sendData);
