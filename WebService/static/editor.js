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
	let defects = image.defects;

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

// setImage(data[0]);
// showDefectsList(data[0]);