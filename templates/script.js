let selectedParcelIds = [];








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


//show list parcel for customer
form_product = document.getElementById('product-customer')
const container = document.getElementById('parcel-customer')
var formCustomer = document.getElementById('product-customer')
var submit = container.querySelector('.but')
submit.addEventListener('click', async (event) => {
    event.preventDefault()
    var formDataCustomer = new FormData(formCustomer)
    var parcelProduct = {}

    for (var [key, value] of formDataCustomer.entries()) {
        parcelProduct[key] = value
    }
    fetch(`http://127.0.0.1:8000/parcel/parcel-customer/?name=${parcelProduct['name']}&last_name=${parcelProduct['last_name']}`).then(res => { return res.json() }).then((data) => {
        var list = document.getElementById('show-product')

        for (var i = 0; i < data.length; i++) {
            var show_price = document.createElement('div')
            var name_item = document.createElement('div')
            var show_count = document.createElement('div')
            var show_total_price = document.createElement('div')
            name_item.innerHTML = `:نام محصول \n ${data[i].nameProduct} `
            name_item.className = 'd-flex border border-black flex-column align-items-center justify-content-center text-center gap-3'

            show_total_price.innerHTML = `:جمع سبد خرید \n ${data[i].TotalPrice}  `
            show_total_price.className = 'd-flex border border-black flex-column align-items-center justify-content-center text-center gap-3'

            show_price.innerHTML = `:قیمت \n ${data[i].price} `

            show_price.className = 'd-flex flex-column align-items-center border border-black justify-content-center text-center gap-3 p-2'

            show_count.innerHTML = `:تعداد محصولات \n ${data[i].count} `
            show_count.className = 'd-flex flex-column align-items-center border border-black justify-content-center text-center p-2'

            list.appendChild(show_price)
            list.appendChild(show_count)
            list.appendChild(show_total_price)
            list.appendChild(name_item)
        }



    });
})



//show list parcel for vendor and submit 2
var form_vendor = document.getElementById('vendor-form')
var submit_name_vendor = form_vendor.querySelector('.vendorButton')
var formVendor = document.getElementById('name-vendor')
submit_name_vendor.addEventListener('click', async (event) => {


    event.preventDefault()
    var formData = new FormData(formVendor)
    var infoVendor = {}
    console.log(formData.values());

    for (var [key, value] of formData.entries()) {
        infoVendor[key] = value
    }


    fetch(`http://127.0.0.1:8000/parcel/parcel-vendor/?name=${infoVendor['name']}&last_name=${infoVendor['last_name']}`).then(res => { return res.json() }).then(
        (data) => {
            let div_items = document.getElementById('show-parcel')
            console.log(data);
            let save_id = []

            for (let i = 0; i < data.length; i++) {
                let show_id = document.createElement('div')
                show_id.innerHTML = `آیدی سفارش \n ${data[i].id}`
                show_id.className = 'd-flex flex-column gap-2 border border-black col-2'
                div_items.appendChild(show_id)
                let name_item2 = document.createElement('div')
                name_item2.innerHTML = `:نام محصول \n ${data[i].nameProduct}`
                div_items.appendChild(name_item2)
                name_item2.className = 'd-flex flex-column gap-2 border border-black col-2'
                let show_price = document.createElement('div')
                show_price.innerHTML = `:قیمت محصول \n ${data[i].price}`
                div_items.appendChild(show_price)
                show_price.className = 'd-flex flex-column gap-2 border border-black col-2'
                let show_total_price = document.createElement('div')
                show_total_price.innerHTML = `:قیمت تمام شده سفارش \n ${data[i].TotalPrice}`
                div_items.appendChild(show_total_price)
                show_total_price.className = 'd-flex flex-column gap-2 border border-black col-2'
                let show_origin = document.createElement('div')
                show_origin.innerHTML = `:منطقه ی دریافتی \n ${data[i].origin}`
                div_items.appendChild(show_origin)
                show_origin.className = 'd-flex flex-column gap-2 border border-black col-2'
                let show_status = document.createElement('div')
                show_status.innerHTML = `:وضعیت سفارش \n ${data[i].status}`
                div_items.appendChild(show_status)
                show_status.className = 'd-flex flex-column gap-2 border border-black col-2'
                let count = document.createElement('div')
                const currentId = data[i].id;
                count.innerHTML = `تعداد  \n ${data[i].count}`
                div_items.appendChild(count)
                show_id.style.cursor = "pointer"
                const parcelIdToSelect = data[i].id;
                let choice_product = document.getElementById('confrim-pro');

                show_id.addEventListener('click', async (event) => {
                    event.preventDefault();

                    const choice_product = document.getElementById('confrim-pro');
                    const index = selectedParcelIds.indexOf(parcelIdToSelect);

                    if (index !== -1) {
                        selectedParcelIds.splice(index, 1);
                        show_id.style.backgroundColor = "transparent";
                        show_id.style.border = "1px solid black";
                    } else {
                        selectedParcelIds.push(parcelIdToSelect);
                        show_id.style.backgroundColor = "lightblue";
                        show_id.style.border = "3px solid blue";
                    }

                    // 🚩 تغییر ۳: فراخوانی تابع جدید برای به‌روزرسانی UI پایین صفحه
                    updateConfirmationArea();

                    console.log("IDهای انتخاب شده:", selectedParcelIds);
                });
            }
            let choice_product = document.getElementById('confrim-pro');
            if (choice_product.innerHTML === '') {

                let button_send_confrim = document.createElement('button');
                let text_button = document.createTextNode('تایید سفارشات انتخاب شده');
                button_send_confrim.appendChild(text_button);

                button_send_confrim.style.cursor = "pointer";
                button_send_confrim.style.width = "200px";
                button_send_confrim.style.height = "100px";

                choice_product.appendChild(button_send_confrim);

                // 🚩 تغییر ۴: اتصال Listener به دکمه Confirm
                button_send_confrim.addEventListener('click', async () => {
                    if (selectedParcelIds.length === 0) {
                        alert("لطفاً حداقل یک سفارش را برای تأیید انتخاب کنید.");
                        return;
                    }

                    const idsString = selectedParcelIds.join(',');
                    const serverIP = 'http://127.0.0.1:8000';
                    const url = `${serverIP}/parcel/submit/?parcel_id=${idsString}`;

                    try {
                        const response = await fetch(url);

                        if (!response.ok) {
                            throw new Error(`HTTP error! status: ${response.status}`);
                        }

                        const result = await response.json();
                        alert(`سفارشات ID ${idsString} با موفقیت تایید شدند.`);

                        // بازنشانی و به‌روزرسانی UI
                        selectedParcelIds = [];
                        // window.location.reload(); 

                    } catch (error) {
                        console.error("خطا در تأیید سفارش:", error);
                        alert("خطا در ارتباط با سرور یا تأیید سفارش.");
                    }
                });
            }

        }
    )
})
function updateConfirmationArea() {
    let choice_product = document.getElementById('confrim-pro');
    choice_product.innerHTML = ''; // پاک کردن محتوای قبلی در هر بار فراخوانی

    if (selectedParcelIds.length > 0) {
        // 1. نمایش IDهای انتخاب شده
        let info_div = document.createElement('div');
        info_div.innerHTML = `
            <strong>${selectedParcelIds.length} سفارش انتخاب شده:</strong> 
            <span>${selectedParcelIds.join(', ')}</span>
        `;
        info_div.className = 'alert alert-info d-flex gap-3 justify-content-between align-items-center';
        choice_product.appendChild(info_div);

        // 2. ساخت دکمه Confirm
        let button_send_confrim = document.createElement('button');
        let text_button = document.createTextNode(`تأیید ${selectedParcelIds.length} سفارش`);
        button_send_confrim.appendChild(text_button);

        button_send_confrim.className = 'btn btn-success mt-2';
        button_send_confrim.style.width = "200px";
        button_send_confrim.style.height = "50px";
        button_send_confrim.style.cursor = "pointer";

        choice_product.appendChild(button_send_confrim);

        // 3. اتصال Listener نهایی به دکمه
        button_send_confrim.addEventListener('click', async () => {
            const idsString = selectedParcelIds.join(',');
            const serverIP = 'http://127.0.0.1:8000/parcel';

            const urlParams = selectedParcelIds.map(id => `parcel_id=${id}`).join('&');

            const url = `${serverIP}/submit/?${urlParams}`;

            try {
                const response = await fetch(url);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const result = await response.json();
                alert(`سفارشات ID ${idsString} با موفقیت تایید شدند.`);

                // پس از موفقیت، آرایه را خالی و UI را به‌روزرسانی کنید
                selectedParcelIds = [];
                updateConfirmationArea();
                // همچنین باید لیست اصلی سفارشات را دوباره fetch کنید
                // window.location.reload(); 
            } catch (error) {
                console.error("خطا در تأیید سفارش:", error);
                alert("خطا در ارتباط با سرور یا تأیید سفارش.");
            }
        });
    }
}


// cancel parcel
var div = document.getElementById('cancel-parcel')
var form_cancel = document.getElementById('cancle-form')
var form_name = document.getElementById('get_name')
var subcancle = div.querySelector('.submit-cancel')
subcancle.addEventListener('click', async (event) => {
    event.preventDefault()
    var show_detail = document.getElementById('show_detail')

    var formData = new FormData(form_cancel)
    var formName = new FormData(form_name)
    var parcel = {}
    for (var [key, value] of formData.entries()) {
        parcel[key] = value
    }
    var parcelName = {}
    for (var [key, value] of formName.entries()) {
        parcelName[key] = value
    }
    fetch(`http://127.0.0.1:8000/parcel/parcel/?parcel_id=${parcel['parcel_id']}&name=${parcelName['name']}&last_name=${parcelName['last_name']}`)
        .then((res) => {
            const jsonPromise = res.json();

            if (res.status == 404) {
                show_detail.innerHTML = 'همچین سفارشی یافت نشد'
            } else if (res.status = 200) {
                return jsonPromise;
            }


        })
        .then(data => {
            var divPrice = document.createElement('div')
            divPrice.innerHTML = data.price
            show_detail.appendChild(divPrice)
            divPrice.className = 'd-flex flex-column border border-black p-2'
            var divName = document.createElement('div')
            divName.innerHTML = data.nameProduct
            show_detail.appendChild(divName)
            divName.className = 'd-flex flex-column border border-black p-2'

            var divTotal = document.createElement('div')
            divTotal.innerHTML = data.TotalPrice
            show_detail.appendChild(divTotal)
            divTotal.className = 'd-flex flex-column border border-black p-2'

            var divCount = document.createElement('div')
            divCount.innerHTML = data.count
            show_detail.appendChild(divCount)
            divCount.className = 'd-flex flex-column border border-black p-2'

            var divStatus = document.createElement('div')
            divStatus.innerHTML = data.status
            show_detail.appendChild(divStatus)
            divStatus.className = 'd-flex flex-column border border-black p-2'

            var divOrigin = document.createElement('div')
            divOrigin.innerHTML = data.origin
            show_detail.appendChild(divOrigin)
            divOrigin.className = 'd-flex flex-column border border-black p-2'


        })
        .catch(error => {
            // خطاها (چه Network و چه خطای 500) در اینجا مدیریت می‌شوند
            console.error('Fetch Error:', error.message);
        });

})


//cancel invoice 

var div = document.getElementById('cancel-invoice')
var form_cancel = document.getElementById('cancle-form_invoice')
var form_name = document.getElementById('get_name_invoice')
var subcancle = div.querySelector('.submit-cancel')
subcancle.addEventListener('click', async (event) => {
    event.preventDefault()
    var show_detail = document.getElementById('show_detail_invoice')

    var formData = new FormData(form_cancel)
    var formName = new FormData(form_name)
    var parcel = {}
    for (var [key, value] of formData.entries()) {
        parcel[key] = value
    }
    console.log(parcel);
    
    var parcelName = {}
    for (var [key, value] of formName.entries()) {
        parcelName[key] = value
    }
    
    fetch(`http://127.0.0.1:8000/parcel/cancel_invoice/?invoice_id=${parcel['invoice_id']}&name=${parcelName['name']}&last_name=${parcelName['last_name']}`)
        .then((res) => {
            const jsonPromise = res.json();

            if (res.status == 404) {
                show_detail.innerHTML = 'همچین سفارشی یافت نشد'
            } else if (res.status = 200) {
                return jsonPromise;
            }


        })
        .then(data => {

            var divCustomerName = document.createElement('div')
            divCustomerName.innerHTML = data.customer_name
            show_detail.appendChild(divCustomerName)
            divCustomerName.className = 'd-flex flex-column border border-black p-2'

            var divInvoiceId = document.createElement('div')
            divInvoiceId.innerHTML = data.invoice_id
            show_detail.appendChild(divInvoiceId)
            divInvoiceId.className = 'd-flex flex-column border border-black p-2'

            var divStatus = document.createElement('div')
            divStatus.innerHTML = data.status
            show_detail.appendChild(divStatus)
            divStatus.className = 'd-flex flex-column border border-black p-2'
        })
        .catch(error => {
            // خطاها (چه Network و چه خطای 500) در اینجا مدیریت می‌شوند
            console.error('Fetch Error:', error.message);
        });

})


var vendorname = document.getElementById('show-vendor')
var formVendorName = document.getElementById('name-vendor-form')
var subName = vendorname.querySelector('.showVendor')
var share = document.getElementById('show-share')
share.style.visibility = "hidden"
subName.addEventListener('click', async (event) => {
    event.preventDefault()
    fetch('http://127.0.0.1:8000/parcel/list_vendor/').then(res => { return res.json() }).then(
        (data) => {
            console.log(data);
            for (var i = 0; i < data.length; i++) {
                let show = document.getElementById('show')
                let vendorId = document.createElement('div')
                vendorId.innerHTML = data[i].id
                show.appendChild(vendorId)
                vendorId.style.cursor = "pointer"
                vendorId.className = 'd-flex flex-column border border-black p-2 col-3'
                let vendorName = document.createElement('div')
                vendorName.innerHTML = data[i].name
                show.appendChild(vendorName)
                vendorName.className = 'd-flex flex-column border border-black p-2 col-3'
                let vendorLastName = document.createElement('div')
                vendorLastName.innerHTML = data[i].last_name
                show.appendChild(vendorLastName)
                vendorLastName.className = 'd-flex flex-column border border-black p-2 col-2'
                let vendorPhone = document.createElement('div')
                vendorPhone.innerHTML = data[i].phone
                show.appendChild(vendorPhone)
                vendorPhone.className = 'd-flex flex-column border border-black p-2 col-2'
                let vendorBalance = document.createElement('div')
                vendorBalance.innerHTML = data[i].balance
                show.appendChild(vendorBalance)
                vendorBalance.className = 'd-flex flex-column border border-black p-2 col-2'
                let list_id = []

                vendorId.addEventListener('click', async (event) => {

                    if (list_id.length === 0) {
                        console.log('خالی است');
                        list_id.push(vendorId)
                        let id = document.getElementById('list')
                        id.innerHTML = vendorId.innerText
                        id.style.border = '1px solid black'
                        share.appendChild(id)
                        event.preventDefault()
                        share.style.visibility = 'visible'
                        list_id.pop()


                    } else {
                        list_id.pop()
                        console.log('خالی نیست');
                        id.innerHTML = ''
                        list_id.length = 0
                        list_id.push(vendorId)
                        let id = document.createElement('div')
                        id.innerHTML = vendorId.innerText
                        id.style.border = '1px solid black'
                        share.appendChild(id)
                        event.preventDefault()
                        share.style.visibility = 'visible'
                    }
                    var form_vendor = document.getElementById('form_vendor_share')
                    var show_share = document.getElementById('show-share')
                    var submitShare = show_share.querySelector('.submitShare')
                   
                    submitShare.addEventListener('click', async (event) => {
                    var formDataShare = new FormData(form_vendor)
                       
                        var parcelshare = {}                    
                          for (var [key, value] of formDataShare) {
                        parcelshare[key] = value
                        console.log(parcelshare);
                        
                          }
                    
                        event.preventDefault()                   
                        fetch(`http://127.0.0.1:8000/parcel/set_share/?vendor_id=${vendorId.innerText}&num=${parcelshare['vendorShare']}`).then(
                            res => { return res.json() }
                        ).then((data) => {
                            var share_vendor = document.getElementById('show-share-vendor')
                            share_vendor.innerHTML = data.message
                            console.log(data);
                            
                        })


                    })
                })


            }
        }
    )
})
//مشخص کردن سهم غرفه دار ها 
