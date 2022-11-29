// html elements
const fileInput = document.querySelector("#file_upload");
const dropAreaBorder = document.querySelector("#custom-file-uploader");
const dropAreaLabel = document.querySelector("#file-upload-label");
const selectContainer = document.querySelector("#select-container");
const selectOutput = document.querySelector("#select-output");
const generateContainer = document.querySelector("#generate-container");
const generateButton = document.querySelector("#generate");
const copyButtons = document.querySelectorAll(".copy-button");

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
  console.log(data);
  const formData = new FormData();
  formData.append("file", data);
  fetch("http://localhost:5000/", {
    method: "POST",
    body: {
      type: "file",
      file: data,
      output: "wt",
    },
  })
    .then((res) => console.log(res))
    .catch((e) => console.log(e));
};
const copyToClipboard = (text) => {
  navigator.clipboard.writeText(text);
};
const findOutputText = (targetElement) => {
  const target = targetElement === "copy-button-1" ? "#output-1" : "#output-2";
  return document.querySelector(target).textContent;
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
const d = [
  {
    _id: "6384787aef2526f5e5cde0a1",
    index: 0,
    guid: "282ae085-d1b8-41b2-86ce-87acf5371983",
    isActive: true,
    balance: "$3,020.50",
    picture: "http://placehold.it/32x32",
    age: 33,
    eyeColor: "green",
    name: "Monique Edwards",
    gender: "female",
    company: "DEVILTOE",
    email: "moniqueedwards@deviltoe.com",
    phone: "+1 (801) 556-2155",
    address: "218 Sackman Street, Coloma, Minnesota, 264",
    about:
      "Eiusmod ut qui est reprehenderit occaecat est laboris occaecat laborum esse qui adipisicing proident cillum. Quis ex magna dolore officia amet eiusmod velit sit irure eu anim. Reprehenderit ullamco sit cillum minim. Esse fugiat reprehenderit ullamco est adipisicing enim quis esse irure mollit. Proident excepteur est officia Lorem. Nostrud id ex aliqua tempor ipsum id sint do voluptate nulla ipsum quis officia.\r\n",
    registered: "2019-01-09T05:21:02 -04:-30",
    latitude: 20.488274,
    longitude: -57.915187,
    tags: ["sint", "dolor", "mollit", "sunt", "non", "eiusmod", "incididunt"],
    friends: [
      {
        id: 0,
        name: "Pate Ingram",
      },
      {
        id: 1,
        name: "Josefa Miles",
      },
      {
        id: 2,
        name: "Imogene Boone",
      },
    ],
    greeting: "Hello, Monique Edwards! You have 1 unread messages.",
    favoriteFruit: "apple",
  },
];
const s = [
  {
    _id: "6384787aef2526f5e5cde0a1",
    index: 0,
    guid: "282ae085-d1b8-41b2-86ce-87acf5371983",
    isActive: true,
    balance: "$3,020.50",
    picture: "http://placehold.it/32x32",
    age: 33,
    eyeColor: "green",
    name: "Monique Edwards",
    gender: "female",
    company: "DEVILTOE",
    email: "moniqueedwards@deviltoe.com",
    phone: "+1 (801) 556-2155",
    address: "218 Sackman Street, Coloma, Minnesota, 264",
    about:
      "Eiusmod ut qui est reprehenderit occaecat est laboris occaecat laborum esse qui adipisicing proident cillum. Quis ex magna dolore officia amet eiusmod velit sit irure eu anim. Reprehenderit ullamco sit cillum minim. Esse fugiat reprehenderit ullamco est adipisicing enim quis esse irure mollit. Proident excepteur est officia Lorem. Nostrud id ex aliqua tempor ipsum id sint do voluptate nulla ipsum quis officia.\r\n",
    registered: "2019-01-09T05:21:02 -04:-30",
    latitude: 20.488274,
    longitude: -57.915187,
    tags: ["sint", "dolor", "mollit", "sunt", "non", "eiusmod", "incididunt"],
    friends: [
      {
        id: 0,
        name: "Pate Ingram",
      },
      {
        id: 1,
        name: "Josefa Miles",
      },
      {
        id: 2,
        name: "Imogene Boone",
      },
    ],
  },
];
const elem = document.querySelector(".output-1");
const elem1 = document.querySelector(".output-2");
elem.innerHTML = prettyPrintJson.toHtml(d, {
  indent: 4,
});
elem1.innerHTML = prettyPrintJson.toHtml(s, {
  indent: 4,
});

dropAreaBorder.addEventListener("drop", dropZoneDropHandler);
selectOutput.addEventListener("change", handleSelectOutput);
generateButton.addEventListener("click", sendData);
copyButtons.forEach((button) =>
  button.addEventListener("click", handleOutputCopy)
);
