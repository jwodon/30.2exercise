const BASE_URL = 'http://localhost:5000/api';

$(document).ready(function () {
    async function getCupcakes() {
        try {
            let response = await axios.get(`${BASE_URL}/cupcakes`);
            const cupcakes = response.data.cupcakes;
            updateCupcakeList(cupcakes);
        } catch (error) {
            console.error('Error fetching cupcakes:', error);
        }
    }

    async function updateCupcakeList(cupcakes) {
        $('#cupcake-list').empty();
        cupcakes.forEach((cupcake) => $('#cupcake-list').append(`<li>${cupcake.flavor}</li>`));
    }

    getCupcakes();

    $('#new-cupcake-form').on('submit', async function (evt) {
        evt.preventDefault();

        let flavor = $('#form-flavor').val();
        let rating = $('#form-rating').val();
        let size = $('#form-size').val();
        let image = $('#form-image').val();

        try {
            const newCupcakeResponse = await axios.post(`${BASE_URL}/cupcakes`, {
                flavor,
                rating,
                size,
                image,
            });

            getCupcakes();
            $('#new-cupcake-form').trigger("reset");
            
        } catch (error) {
            console.error('Error creating cupcake:', error);
        }
    });
});
