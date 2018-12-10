document.addEventListener('DOMContentLoaded', () => {

    var form = document.querySelector('#post');
    var message = document.querySelector('#message');
    image_file = document.querySelector('#file_image');
    
    // Validate file size.
    form.onsubmit = () => {
        image_file_size = image_file.files[0].size;
        const max_size = 2.5; // MB
        
        console.log(image_file_size);

        if (image_file_size > 1024*1024*max_size) {
            message.innerHTML = `The file size is bigger than ${max_size} MB.`;
            return false;
        }
        return true;
    };
});