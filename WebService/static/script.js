'use strict';


const d = document;

let imagesWithDefects; 


let currentDefect = {
    class : undefined,
    index : undefined
};

let newDefect = [];

let currentImage;


const ctx = canvas.getContext('2d');

let isDrawing = false;
let startX, startY;
let img;


function drawRectangle(x1, y1, w, h) {
    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
    ctx.strokeStyle = 'red';
    ctx.lineWidth = 2;
    ctx.strokeRect(x1, y1, w, h);
}


function setImage(image) {
    currentImage = image;

    img = new Image();
    img.src = image.src;

    img.onload = () => {
        canvas.width = img.width / 2;
        canvas.height = img.height / 2;

        defectsContainer.style.maxHeight = `${canvas.height + 40}px`; 

        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
    }

    editor.style.display = 'flex';
    form.style.display = 'none';
}


function saveChanges() {
    currentImage.defects[currentDefect.class][currentDefect.index] = newDefect; 
}


canvas.addEventListener('mousedown', (event) => {
    startX = event.offsetX;
    startY = event.offsetY;
    isDrawing = true;
});


canvas.addEventListener('mousemove', (event) => {
    if (isDrawing) {
        const currentX = event.offsetX;
        const currentY = event.offsetY;
        const width = currentX - startX;
        const height = currentY - startY;

        drawRectangle(startX, startY, width, height);
        newDefect = [2 * startX, 2 * startY, 2 * width, 2 * height];
    }
});


canvas.addEventListener('mouseup', () => {
    isDrawing = false;
});


canvas.addEventListener('mouseleave', () => {
    isDrawing = false;
});

        
function showDefectsList(image) {
    let defects = image.defect;

    for (const className in defects) {
        const header = d.createElement('h3');
        header.textContent = className;
        defectsContainer.appendChild(header);

        const ul = d.createElement('ul');

        defects[className].forEach((defect, index) => {
            const li = d.createElement('li');

            const radio = d.createElement('input');
            radio.type = 'radio';
            radio.name = 'editor';
            radio.id = `${className}-${index}`;
            radio.onclick = () => {
                currentDefect.class = className;
                currentDefect.index = index;
                drawRectangle(
                    defect[0] / 2,
                    defect[1] / 2,
                    defect[2] / 2,
                    defect[3] / 2);
            };

            const label = d.createElement('label');
            label.htmlFor = radio.id;
            label.textContent = `дефект №${index + 1}`;

            li.appendChild(radio);
            li.appendChild(label);
            ul.appendChild(li);
        });

        defectsContainer.appendChild(ul);
    }
}



let uploadImages = new Array();


function addImages(images) {
    for (let i = 0; i < images.length; i++)
        uploadImages.push(images[i]);

    showPreviews();
}


function removeImage(index) {
    uploadImages.splice(index, 1);
    showPreviews();
}


function showEditor(i) {
    let curImage = imagesWithDefects[i];
    editor.style.display = 'flex';
    currentImage = curImage;
    setImage(curImage);
    showDefectsList(curImage);
}


function showImagesWithDefects() {
    imgsPreview.innerHTML = '';

    for (let i = 0; i < imagesWithDefects.length; i++) {
        imagesWithDefects[i].src = 'http://127.0.0.1:8000/' + imagesWithDefects[i].src;
        const src = imagesWithDefects[i].src;
        imgsPreview.innerHTML += `
            <li>
                <img src="${src}">
                <input 
                    type="button" 
                    value="Редактировать" 
                    onclick="showEditor(${i})">
            </li>
        `
    }
}


function showPreviews() {
    imgsPreview.innerHTML = '';

    for (let i = 0; i < uploadImages.length; i++) {
        const imageUrl = URL.createObjectURL(uploadImages[i]);
        imgsPreview.innerHTML += `
            <li>
                <img src="${imageUrl}">
                <input 
                    type="button" 
                    value="Удалить" 
                    onclick="removeImage(${i})">
            </li>
        `
    }
}


function validate() {
    if (serialNumInput.value == '') {
        serialNumInput.style.border = '2px solid red';
        alert('Серийный номер не указан!');
        return false;
    }

    if (uploadImages.length == 0) {
        alert('Фотографии не добавлены!');
        return false;
    }

    return true;
}


uploadButton.addEventListener('click', () => {
    const fileInput = d.createElement('input');
    fileInput.type = 'file';
    fileInput.multiple = true;
    fileInput.accept = 'image/*'
    fileInput.style.display = 'none';

    fileInput.addEventListener('change', () => {
        addImages(fileInput.files);
    });

    fileInput.click();
});


submitButton.addEventListener('click', async function() {
    if (!validate()) return;

    const formData = new FormData();

    for (let i = 0; i < uploadImages.length; i++)
        formData.append('images', uploadImages[i]);

    formData.append('number', serialNumInput.value);

    form.style.display = 'none';

    try {
        const response = await fetch('/upload/', {
            method: 'POST',
            body: formData
        });

        imagesWithDefects = await response.json();
        imagesWithDefects = JSON.parse(imagesWithDefects);
        showImagesWithDefects();

    } catch (error) {
        alert('Ошибка соединения');
    }
});

async function send() {
    try {
        const response = await fetch('/report/' + serialNumInput.value + '/', {
            method: 'POST',
            body: JSON.stringify(imagesWithDefects)
        });

        let report = await response.json();
        editor.style.display = 'none';
        imgsPreview.style.display = 'none';

    } catch (error) {
        alert('Ошибка соединения');
    }
}