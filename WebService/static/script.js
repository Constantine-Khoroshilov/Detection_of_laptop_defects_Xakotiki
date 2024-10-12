'use strict';


const d = document;


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

    try {
        const response = await fetch('/upload/', {
            method: 'POST',
            body: formData
        });

        let result = await response.text();
        d.getElementById('response').innerText = `Файл: ${result}`;

    } catch (error) {
        d.getElementById('response').innerText = `Ошибка: ${error.message}`;
    }
});