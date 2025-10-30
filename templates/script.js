let selectedParcelIds = [];








// show all product 
fetch('http://127.0.0.1:8000/parcel/vendor/list_product/')
    .then((res) => {
        console.log(res);
        
        return res.json()
    })
.then(products => {

    console.log(products);
    
    const form = document.getElementById('form-name')
    const container = document.getElementById('product_list_container');
    var name_vendor = []
    var last_name = []
    var productLIst = document.getElementById('product_list')
    let addParcel = {}

    for (let i = 0; i < products.length; i++) {
        let countProduct = 0
        
        var last_name_vendor = document.createElement('div')
        var name = document.createElement('div')
        let name_product = document.createElement('div')
        let price_product = document.createElement('div')
        var sortName = document.createElement('div')
        var sortProduct = document.createElement('div')
        var IconMin = document.createElement('div')
        var IconPlus = document.createElement('div')
        let count = document.createElement('div')
        count.innerHTML = countProduct
        IconPlus.innerHTML = '<i class="bi bi-plus"></i>'
        IconMin.innerHTML = '<i class="bi bi-dash"></i>'
        
        const nameVendorian = products[i].name_vendor + '-' + products[i].last_name_vendor;
        
        const newProduct = {
            product_name: products[i].name,
            price: products[i].price,
            count: 0
        };

        // 🎯 ثبت اولیه محصول و مرجع‌دهی (فقط یک بار)
        if (!addParcel[nameVendorian]) {
            addParcel[nameVendorian] = [];
        }
        addParcel[nameVendorian].push(newProduct);
        const productReference = newProduct;

        var lastNameVendorian = products[i].last_name_vendor
        
        if ((name_vendor === 0 && last_name === 0) || ((name_vendor.indexOf(products[i].name)) && (last_name.indexOf(products[i].last_name_vendor)))) {
            name_vendor.push(products[i].name_vendor)
            last_name.push(products[i].last_name_vendor)
            name.innerHTML = `${products[i].name_vendor}-${products[i].last_name_vendor} :نام غرفه دار `

            sortName.appendChild(name)

            name_product.innerHTML = products[i].name
            price_product.innerHTML = products[i].price
            sortProduct.appendChild(IconPlus)
            IconMin.style.cursor = "pointer"
            IconPlus.style.cursor = "pointer"

            IconPlus.addEventListener('click', (event) => {
                event.preventDefault()

                countProduct = countProduct + 1
                count.innerHTML = countProduct
                
                // به‌روزرسانی مرجع count
                productReference.count = countProduct; 

            })
            sortProduct.appendChild(count)
            sortProduct.appendChild(IconMin)
            IconMin.addEventListener('click', async (event) => {
                event.preventDefault()

                if (countProduct != 0) {
                    countProduct = countProduct - 1
                    count.innerHTML = countProduct
                    
                    // به‌روزرسانی مرجع count
                    productReference.count = countProduct; 

                } else {
                    count.innerHTML = 0
                    
                    // به‌روزرسانی مرجع count به صفر
                    productReference.count = 0; 
                }
            })

            sortProduct.appendChild(price_product)
            sortProduct.appendChild(name_product)
            container.appendChild(sortName)
            container.appendChild(sortProduct)

            container.className = 'd-flex flex-column border border-black gap-2 col-12'
            sortName.className = 'd-flex gap-2 border border-black'
            sortProduct.className = 'd-flex gap-2 border border-black '
        } else {
            name_product.innerHTML = products[i].name
            price_product.innerHTML = products[i].price
            container.appendChild(name_product)
            container.appendChild(price_product)
            sortProduct.appendChild(IconPlus)
            sortProduct.appendChild(count)
            sortProduct.appendChild(IconMin)
            sortProduct.appendChild(price_product)
            sortProduct.appendChild(name_product)
            container.appendChild(sortProduct)
            container.className = 'd-flex gap-2 col-12'
            sortProduct.className = 'd-flex gap-2'
            IconMin.style.cursor = "pointer"
            IconPlus.style.cursor = "pointer"
            
            IconPlus.addEventListener('click', (event) => {
                event.preventDefault()

                countProduct = countProduct + 1
                count.innerHTML = countProduct
                
                // به‌روزرسانی مرجع count
                productReference.count = countProduct;
            })

            IconMin.addEventListener('click', async (event) => {
                event.preventDefault()
                if (countProduct != 0) {
                    countProduct = countProduct - 1
                    count.innerHTML = countProduct
                    
                    // به‌روزرسانی مرجع count
                    productReference.count = countProduct;

                } else {
                    count.innerHTML = 0
                    
                    // به‌روزرسانی مرجع count به صفر
                    productReference.count = 0;
                }
            })
        }
    }
    
    var parcelName = {}
    var FormName = document.getElementById('form-name')
    var sub = productLIst.querySelector('.confirmListProduct')
    sub.addEventListener('click', async (event) => {
        console.log(addParcel);

        var formData = new FormData(FormName)
        for (var [key, value] of formData.entries()) {
            parcelName[key] = value
        }

        fetch(`http://127.0.0.1:8000/parcel/add_parcel/?name=${parcelName['name']}&last_name=${parcelName['last_name']}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },

            body: JSON.stringify({
                data: addParcel,
            }),

        }).then(res => { return res.json() }).then(data => {
                    console.log(data);
                    
        })

    })
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

    for (var [key, value] of formData.entries()) {
        infoVendor[key] = value
    }


    fetch(`http://127.0.0.1:8000/parcel/parcel-vendor/?name=${infoVendor['name']}&last_name=${infoVendor['last_name']}`).then(res => { return res.json() }).then(
        (data) => {
            let div_items = document.getElementById('show-parcel')

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

                    updateConfirmationArea();

                });
            }
            let choice_product = document.getElementById('confrim-pro');
            if (choice_product.innerHTML == '') {

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
                let vendor_Phone = document.createElement('div')
                vendor_Phone.innerHTML = data[i].phone
                show.appendChild(vendor_Phone)
                vendor_Phone.className = 'd-flex flex-column border border-black p-2 col-2'
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

                        }

                        event.preventDefault()
                        fetch(`http://127.0.0.1:8000/parcel/set_share/?vendor_id=${vendorId.innerText}&num=${parcelshare['vendorShare']}`).then(
                            res => { return res.json() }
                        ).then((data) => {
                            var share_vendor = document.getElementById('show-share-vendor')
                            share_vendor.innerHTML = data.message

                        })


                    })
                })


            }
        }
    )
})
//مشخص کردن سهم غرفه دار ها 



//ارسال مرسوله توسط غرفه دار 

let formSend = document.getElementById('sendParcel')
let butClick = formSend.querySelector('.send-click')
butClick.className='border border-danger'
let parcelSend = {}
butClick.addEventListener('click', async (event) => {
    event.preventDefault()
    let formData = new FormData(formSend)
    for (var [key, value] of formData.entries()) {
        parcelSend[key] = value
    }
    fetch(`http://127.0.0.1:8000/parcel/parcel-vendor/?name=${parcelSend['name']}&last_name=${parcelSend['last_name']}`).then(async res => {
        
        if (res.status == 404) {
            var json = await res.json()
            const error = json.detail
            if (error == 'vendor is not exist') {
                var notName = document.getElementById('showSend')
                notName.innerHTML = error
            }
        }
        return res.json()

    }).then((data) => {
        console.log(data);
        
        var showParcel = document.getElementById('showSend')
        for (var i = 0; i < data.length; i++) {
            if (data[i].status == 'PARCEL_CONFIRM_BY_VENDOR') {


                let nameProduct = data[i].nameProduct
                let divNameProduct = document.createElement('div')
                divNameProduct.innerHTML = nameProduct

                let priceProduct = data[i].price
                let divPrice = document.createElement('div')
                divPrice.innerHTML = priceProduct

                let totalPriceProduct = data[i].TotalPrice
                let divTotal = document.createElement('div')
                divTotal.innerHTML = totalPriceProduct

                let countProduct = data[i].count
                let divCountProduct = document.createElement('div')
                divCountProduct.innerHTML = countProduct

                let statusProduct = data[i].status
                let divStatus = document.createElement('div')
                divStatus.innerHTML = statusProduct

                let Button = document.createElement('button')
                Button.innerText = 'click me'

                Button.style.height = '50px'
                var showSend = document.createElement('div')
                showSend.appendChild(divNameProduct)
                showSend.appendChild(divPrice)
                showSend.appendChild(divCountProduct)
                showSend.appendChild(divTotal)
                showSend.appendChild(divStatus)
                showSend.appendChild(Button)
                showSend.className = ' d-flex col-3 flex-column gap-2 border border border-black '
                showParcel.className = 'row d-flex p-2'

                showParcel.appendChild(showSend)
                Button.addEventListener('click', async (event) => {
                    event.preventDefault()
                    fetch(`http://127.0.0.1:8000/parcel/post_vendor/?name=${parcelSend['name']}&last_name=${parcelSend['last_name']}`).then(res => {
                        
                        return res.json()
                    }).then((data) => {
                            
                            for (var i =0 ; i<data.length; i++){
                            showParcel.innerHTML = ''
                            var showSend = document.createElement('div')
                            let getStatus = data[i].statusDelivery
                            let status = document.createElement('div')
                            status.innerHTML = getStatus
                            let name = document.createElement('div')
                            let getName = data.name_customer
                            name.innerHTML = getName
                            let lastName = document.createElement('div')
                            let getLast = data.lastName_customer
                            lastName.innerHTML = getLast
                            let id = document.createElement('div')
                            let getId = data.parcel_id
                            id.innerHTML = getId
                            let price = document.createElement('div')
                            let getPrice = data.price_delivery
                            price.innerHTML = getPrice
                            showSend.appendChild(name)
                            showSend.appendChild(lastName)
                            showSend.appendChild(id)
                            showSend.appendChild(price)
                            showSend.className = ' d-flex flex-column '
                            showParcel.appendChild(showSend)}
                            alert('سفارش در حالت ارسال قرار گرفت ')
                            console.log(data);
                            
                        }
                    )
                })

            }
        console.log(data);
   
        }
    })

})