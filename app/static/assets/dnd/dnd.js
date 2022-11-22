let fileInput = document.querySelector('#file_upload');

fileInput.addEventListener("drop",dropZoneDropHandler);

function dropZoneDropHandler(e) {
  let link = e.dataTransfer.getData('URL');
  console.log(link);
  document.querySelector('.file-name-get').value = link;

  e.preventDefault();
  e.stopPropagation();
}
