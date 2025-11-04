let selectedParcelIds = [];

// نمایش همه محصولات
fetch('http://127.0.0.1:8000/parcel/vendor/list_product/')
    .then((res) => res.json())
    .then(products => {
        // 💡 FIX 1: استخراج شیء داده اصلی از آرایه (products[0])
        const vendorData = products; 

        let form = document.getElementById('form-name');
        let container = document.getElementById('product_list_container');
        let productList = document.getElementById('product_list');
        let addParcel = {}; 
        console.log(products);
        
        for (let i = 0; i < Object.keys(products).length; i++) {
            const nameVendorian = vendorData[i][i].nameVendor + '-' + vendorData[i][i].lastNameVendor; 

        if (!addParcel[nameVendorian]) {
            addParcel[nameVendorian] = [];
        }
            let countProduct = 0; 
        console.log(vendorData[i][i]);
            
            const newProduct = {
                product_name: vendorData[i][i].nameProduct, 
                price: vendorData[i][i].price, 
                count: 0 
            };

            // ذخیره ارجاع به این شیء در ساختار addParcel
            addParcel[nameVendorian].push(newProduct);
            let productReference = newProduct; 

            // ... (کدهای DOM) ...
            
            let divFull = document.createElement('div')
            let nameProduct = document.createElement('div')
            nameProduct.innerHTML = vendorData[i][i].nameProduct
            divFull.appendChild(nameProduct)

            let priceProduct = document.createElement('div')
            priceProduct.innerHTML = vendorData[i][i].price
            divFull.appendChild(priceProduct)

            let icons = document.createElement('div')
            let IconPlus = document.createElement('div')
            IconPlus.innerHTML = '<i class="bi bi-plus"></i>'
            icons.appendChild(IconPlus)

            let count = document.createElement('div')
            count.innerHTML = countProduct
            icons.appendChild(count)


            let IconMin = document.createElement('div')
            IconMin.innerHTML = '<i class="bi bi-dash"></i>'
            icons.appendChild(IconMin)

            icons.className = 'd-flex gap-3'
            divFull.appendChild(icons)
            divFull.className = 'd-flex flex-column gap-3 align-items-center'
            
            // --- Event Listeners ---
            IconPlus.addEventListener('click', (event) => {
                event.preventDefault();
                countProduct++;
                count.innerHTML = countProduct;
                // به‌روزرسانی مقدار count در شیء اصلی addParcel
                productReference.count = countProduct; 
            });
            IconPlus.style.cursor = "pointer"

            IconMin.addEventListener('click', (event) => {
                event.preventDefault();
                if (countProduct > 0) countProduct--;
                count.innerHTML = countProduct;
                productReference.count = countProduct; 
            });
            IconMin.style.cursor = "pointer"

            divFull.className = 'd-flex flex-column gap-3'
            container.appendChild(divFull)
            container.className = 'd-flex gap-3'
        }

        // --- منطق ارسال ---
        let formName = document.getElementById('form-name');
        let sub = productList.querySelector('.confirmListProduct');
        sub.addEventListener('click', async (event) => {
            event.preventDefault();
            let parcelName = {};
            const formData = new FormData(formName);
            
            // 💡 FIX: حذف آلودگی. فقط اطلاعات فرم در parcelName ذخیره می‌شود.
            for (const [key, value] of formData.entries()) {
                parcelName[key] = value
                // ❌ خطای زیر حذف شد: addParcel[key]=value
            };

            let finalAddParcel = {};
            for (const vendorKey in addParcel) {
                if (addParcel.hasOwnProperty(vendorKey) && Array.isArray(addParcel[vendorKey])) {
                    const filteredProducts = addParcel[vendorKey].filter(product => product.count > 0);
                    if (filteredProducts.length > 0) {
                        finalAddParcel[vendorKey] = filteredProducts;
                    }
                }
            }
            
            // بررسی اینکه حداقل یک محصول انتخاب شده باشد
            if (Object.keys(finalAddParcel).length === 0) {
                alert("لطفاً حداقل یک محصول را برای خرید انتخاب کنید.");
                return;
            }

            fetch(`http://127.0.0.1:8000/parcel/add_parcel/?name=${parcelName['name']}&last_name=${parcelName['last_name']}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                // ارسال داده‌های نهایی و فیلتر شده
                body: JSON.stringify({ data: finalAddParcel }) 
            })
                .then( (res) => {
                    if(res.status === 400){
                        return res.json().then(errorData => {
                            alert(`خطا: ${errorData.detail}`);
                            return Promise.reject(errorData); // برای پرش به catch
                        });
                    }
                    if(!res.ok){
                         throw new Error(`HTTP error! status: ${res.status}`);
                    }
                    return res.json();
                })
                .then(data => {
                    console.log('✅ ثبت مرسوله:', data)
                    
                })
                .catch(err => {
                    if (err.detail) {
                        // خطا قبلا مدیریت شده است
                        return; 
                    }
                    console.error('❌ خطا در ثبت مرسوله:', err)
                    alert('خطای ناشناخته در ثبت مرسوله رخ داد.')
                });
        });
    });
// نمایش سفارشات مشتری
const parcelContainer = document.getElementById('parcel-customer');
const formCustomer = document.getElementById('product-customer');
const submit = parcelContainer.querySelector('.but');
submit.addEventListener('click', async (event) => {
    event.preventDefault();
    const formDataCustomer = new FormData(formCustomer);
    const parcelProduct = {};
    for (const [key, value] of formDataCustomer.entries()) parcelProduct[key] = value;

    fetch(`http://127.0.0.1:8000/parcel/parcel-customer/?name=${parcelProduct['name']}&last_name=${parcelProduct['last_name']}`)
        .then(res => res.json())
        .then((data) => {
            const list = document.getElementById('show-product');
            list.innerHTML = '';
            for (let i = 0; i < data.length; i++) {
                const name_item = document.createElement('div');
                name_item.innerHTML = `نام محصول: ${data[i].nameProduct}`;
                const show_price = document.createElement('div');
                show_price.innerHTML = `قیمت: ${data[i].price}`;
                const show_count = document.createElement('div');
                show_count.innerHTML = `تعداد: ${data[i].count}`;
                const show_total_price = document.createElement('div');
                show_total_price.innerHTML = `جمع کل: ${data[i].TotalPrice}`;
                list.append(name_item, show_price, show_count, show_total_price);
            }
        });
});

// نمایش سفارشات غرفه‌دار
const form_vendor = document.getElementById('vendor-form');
const submit_name_vendor = form_vendor.querySelector('.vendorButton');
const formVendor = document.getElementById('name-vendor');

submit_name_vendor.addEventListener('click', async (event) => {
    event.preventDefault();
    const formData = new FormData(formVendor);
    const infoVendor = {};
    for (const [key, value] of formData.entries()) infoVendor[key] = value;

    fetch(`http://127.0.0.1:8000/parcel/parcel-vendor/?name=${infoVendor['name']}&last_name=${infoVendor['last_name']}`)
        .then(res => res.json())
        .then((data) => {
            const div_items = document.getElementById('show-parcel');
            div_items.innerHTML = '';
            selectedParcelIds = [];

            data.forEach((parcel) => {
                const parcelIdToSelect = parcel.id;
                const card = document.createElement('div');
                card.className = 'border border-black p-2 m-2 col-3';
                card.style.cursor = "pointer";
                card.innerHTML = `
                    <div><strong>ID:</strong> ${parcel.id}</div>
                    <div>محصول: ${parcel.nameProduct}</div>
                    <div>قیمت: ${parcel.price}</div>
                    <div>وضعیت: ${parcel.status}</div>
                `;

                card.addEventListener('click', (event) => {
                    event.preventDefault();
                    event.stopPropagation();

                    const index = selectedParcelIds.indexOf(parcelIdToSelect);
                    if (index !== -1) {
                        selectedParcelIds.splice(index, 1);
                        card.style.backgroundColor = "transparent";
                        card.style.border = "1px solid black";
                    } else {
                        selectedParcelIds.push(parcelIdToSelect);
                        card.style.backgroundColor = "#e0f7fa";
                        card.style.border = "3px solid #00bcd4";
                    }
                    updateConfirmationAreaVendor();
                });

                div_items.appendChild(card);
            });

            updateConfirmationAreaVendor();
        });
});

// ✅ تابع نهایی تأیید سفارش‌ها
function updateConfirmationAreaVendor() {
    const choice_product = document.getElementById('confrim-pro');
    choice_product.innerHTML = '';

    if (selectedParcelIds.length > 0) {
        const info_div = document.createElement('div');
        info_div.innerHTML = `
            <strong>${selectedParcelIds.length} سفارش انتخاب شده:</strong>
            <span>${selectedParcelIds.join(', ')}</span>
        `;
        info_div.className = 'alert alert-info d-flex gap-3 justify-content-between align-items-center';
        choice_product.appendChild(info_div);

        const button_send_confrim = document.createElement('button');
        button_send_confrim.textContent = `تأیید ${selectedParcelIds.length} سفارش`;
        button_send_confrim.className = 'btn btn-success mt-2';
        button_send_confrim.style.width = "200px";
        button_send_confrim.style.height = "50px";
        button_send_confrim.style.cursor = "pointer";
        choice_product.appendChild(button_send_confrim);

        button_send_confrim.addEventListener('click', async (event) => {
            event.preventDefault();
            event.stopPropagation();

            const urlParams = selectedParcelIds.map(id => `parcel_id=${encodeURIComponent(id)}`).join('&');
            const url = `http://127.0.0.1:8000/parcel/submit/?${urlParams}`;

            try {
                const response = await fetch(url);
                if (!response.ok) {
                    const err = await response.json();
                    throw new Error(err.detail || `HTTP Error ${response.status}`);
                }
                const result = await response.json();
                alert(`✅ سفارشات ID ${selectedParcelIds.join(', ')} با موفقیت تأیید شدند.`);
                selectedParcelIds = [];
                updateConfirmationAreaVendor();
            } catch (error) {
                console.error("❌ خطا در تأیید سفارش:", error);
                alert(`خطا: ${error.message}`);
            }
        });
    }
}

// ✅ بخش مدیریت نمایش لیست غرفه‌داران و تعیین سهم
const vendorname = document.getElementById('show-vendor');
const formVendorName = document.getElementById('name-vendor-form');
const subName = vendorname.querySelector('.showVendor');
const share = document.getElementById('show-share');
share.style.visibility = "hidden";

subName.addEventListener('click', async (event) => {
    event.preventDefault();
    fetch('http://127.0.0.1:8000/parcel/list_vendor/')
        .then(res => res.json())
        .then((data) => {
            const show = document.getElementById('show');
            show.innerHTML = '';
            data.forEach((vendor) => {
                const vendorDiv = document.createElement('div');
                vendorDiv.className = 'd-flex flex-column border border-black p-2 col-3';
                vendorDiv.innerHTML = `${vendor.id} - ${vendor.name} ${vendor.last_name}`;
                vendorDiv.style.cursor = "pointer";

                vendorDiv.addEventListener('click', (event) => {
                    event.preventDefault();
                    const idDiv = document.getElementById('list');
                    idDiv.innerHTML = vendor.id;
                    idDiv.style.border = '1px solid black';
                    share.style.visibility = 'visible';

                    const form_vendor = document.getElementById('form_vendor_share');
                    const submitShare = form_vendor.querySelector('.submitShare');
                    submitShare.addEventListener('click', async (event) => {
                        event.preventDefault();
                        const formDataShare = new FormData(form_vendor);
                        const shareValue = formDataShare.get('vendorShare');
                        fetch(`http://127.0.0.1:8000/parcel/set_share/?vendor_id=${vendor.id}&num=${shareValue}`)
                            .then(res => res.json())
                            .then(data => {
                                const share_vendor = document.getElementById('show-share-vendor');
                                share_vendor.innerHTML = data.message;
                            });
                    }, { once: true });
                });

                show.appendChild(vendorDiv);
            });
        });
});

// ارسال مرسوله توسط غرفه‌دار
const formSend = document.getElementById('sendParcel');
const butClick = formSend.querySelector('.send-click');
butClick.className = 'border border-danger';
butClick.addEventListener('click', async (event) => {
    event.preventDefault();
    const formData = new FormData(formSend);
    const parcelSend = {};
    for (const [key, value] of formData.entries()) parcelSend[key] = value;

    const res = await fetch(`http://127.0.0.1:8000/parcel/parcel-vendor/?name=${parcelSend['name']}&last_name=${parcelSend['last_name']}`);
    if (res.status === 404) {
        const json = await res.json();
        if (json.detail === 'vendor is not exist') {
            document.getElementById('showSend').innerHTML = json.detail;
            return;
        }
    }
    const data = await res.json();
    const showParcel = document.getElementById('showSend');
    showParcel.innerHTML = '';

    data.forEach((item) => {
        if (item.status === 'PARCEL_CONFIRM_BY_VENDOR') {
            const div = document.createElement('div');
            div.className = 'd-flex flex-column gap-2 border border-black p-2';
            div.innerHTML = `
                <div>نام محصول: ${item.nameProduct}</div>
                <div>قیمت: ${item.price}</div>
                <div>تعداد: ${item.count}</div>
                <div>جمع کل: ${item.TotalPrice}</div>
                <div>وضعیت: ${item.status}</div>
            `;
            const button = document.createElement('button');
            button.textContent = 'ارسال مرسوله';
            button.addEventListener('click', async () => {
                const res = await fetch(`http://127.0.0.1:8000/parcel/post_vendor/?name=${parcelSend['name']}&last_name=${parcelSend['last_name']}`);
                const data = await res.json();
                alert('سفارش در حالت ارسال قرار گرفت ✅');
                console.log(data);
            });
            div.appendChild(button);
            showParcel.appendChild(div);
        }
    });
});
