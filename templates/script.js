
//cancel product
// function buy_items() { }
// fetch('http://127.0.0.1:8000/parcel/parcel/8')
//     .then(response => {
//         const jsonPromise = response.json();

//         if (!response.ok) {
//             return jsonPromise.then(err => {
//                 throw new Error(JSON.stringify(err));
//             });
//         }

//         return jsonPromise;
//     })
//     .then(data => {
//         console.log("Success Data:", data);
//         var price = data.price
//         var name = data.nameProduct
//         var count = data.count
//         var status = data.status
//         document.getElementById('cancelName').innerHTML = name
//         document.getElementById('cancelCount').innerHTML = count
//         if (status == 'cancel') {
//             document.getElementById('cancelStatus').innerHTML = status

//         }
//         document.getElementById('cancelPrice').innerHTML = price



//     })
//     .catch(error => {
//         // خطاها (چه Network و چه خطای 500) در اینجا مدیریت می‌شوند
//         console.error('Fetch Error:', error.message);
//     });
// show all product 
fetch('http://127.0.0.1:8000/parcel/vendor/list_product/')
    .then((res) => res.json())
    .then(products => {
        const form = document.getElementById('form-name')

        const container = document.getElementById('product_list_container');
        container.innerHTML = '';
        console.log(products);



        products.forEach(product => {
            let currentCount = 1;

            const productCard = document.createElement('div');
            productCard.className = 'product_list_container d-flex flex-column gap-3';

            productCard.innerHTML = `
                <span class='d-flex gap-3'>${product.name} (قیمت: ${product.price})</span>
                <p class='d-flex gap-2'> ${product.name_vendor} ${product.last_name_vendor} <strong>:نام فروشنده</strong></p>
                
                <div class='add-min d-flex flex-column gap-4' data-product-id="${product.id}">
                    <div class='d-flex gap-3'>
                    <div class='plus-btn'><i class="bi bi-plus-lg"></i></div>
                    
                    <span class='count-display'>${currentCount}</span> 
                    
                    <div class='min-btn'><i class="bi bi-dash-lg"></i></div>
                    </div>
                     <button class='but'>خرید جنس</button>
                </div>
                
                <hr>
            `;

            container.appendChild(productCard);

            const plusButton = productCard.querySelector('.plus-btn');
            const minButton = productCard.querySelector('.min-btn');
            const countDisplay = productCard.querySelector('.count-display');
            const subbutton = productCard.querySelector('.but')
            plusButton.addEventListener('click', () => {
                currentCount++;
                countDisplay.textContent = currentCount;
                console.log(`Product ID ${product.id} count: ${currentCount}`);
            });

            minButton.addEventListener('click', () => {
                if (currentCount > 1) { // جلوگیری از منفی شدن شمارنده
                    currentCount--;
                    countDisplay.textContent = currentCount;
                    console.log(`Product ID ${product.id} count: ${currentCount}`);
                }
            });

            const API_URL = 'http://127.0.0.1:8000/parcel/add_parcel/';
            subbutton.addEventListener('click', async (event) => {
                event.preventDefault()
                var formData = new FormData(form)
                var dicName = {}
                for (var [key, value] of formData.entries()) {
                    dicName[key] = value

                }
                const parcel = {
                    'vendor_name': product.name_vendor,
                    'last_name_vendor': product.last_name_vendor,

                    'invoice': 1,
                    'status': 'تایید',
                    'count': currentCount,

                    'product_id': product.name,
                    'customer_name': dicName,
                };

                console.log("Sending Parcel Data:", parcel);

                try {
                    const response = await fetch(API_URL, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(parcel),
                    });
                    if (!response.ok) {
                        const errorData = await response.json();
                        throw new Error(`Server Error ${response.status}: ${errorData.detail || 'Failed to process'}`);
                    }

                    var data = await response.json();
                    console.log("Success:", data);
                    alert(`محصول ${product.name} با موفقیت ثبت شد.`);
                } catch (error) {
                    console.error("Fetch Error:", error);
                    console.log(`خطا در ثبت خرید: ${error.message}`);

                                    }
            })

        });
    });




