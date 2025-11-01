let selectedParcelIds = [];

// نمایش همه محصولات
fetch('http://127.0.0.1:8000/parcel/vendor/list_product/')
    .then((res) => res.json())
    .then(products => {
        const form = document.getElementById('form-name');
        const container = document.getElementById('product_list_container');
        const productList = document.getElementById('product_list');
        let addParcel = {};

        for (let i = 0; i < products.length; i++) {
            let countProduct = 0;

            const IconMin = document.createElement('div');
            const IconPlus = document.createElement('div');
            const count = document.createElement('div');
            IconPlus.innerHTML = '<i class="bi bi-plus"></i>';
            IconMin.innerHTML = '<i class="bi bi-dash"></i>';
            count.innerHTML = countProduct;
            IconPlus.style.cursor = "pointer";
            IconMin.style.cursor = "pointer";

            const nameVendorian = products[i].name_vendor + '-' + products[i].last_name_vendor;
            if (!addParcel[nameVendorian]) {
                addParcel[nameVendorian] = [];
            }

            const newProduct = {
                product_name: products[i].name,
                price: products[i].price,
                count: 0
            };
            addParcel[nameVendorian].push(newProduct);
            const productReference = newProduct;

            const sortProduct = document.createElement('div');
            sortProduct.className = 'd-flex gap-2 border border-black p-2';

            const name_product = document.createElement('div');
            name_product.innerHTML = products[i].name;
            const price_product = document.createElement('div');
            price_product.innerHTML = products[i].price;

            sortProduct.appendChild(name_product);
            sortProduct.appendChild(price_product);
            sortProduct.appendChild(IconPlus);
            sortProduct.appendChild(count);
            sortProduct.appendChild(IconMin);
            container.appendChild(sortProduct);

            IconPlus.addEventListener('click', (event) => {
                event.preventDefault();
                countProduct++;
                count.innerHTML = countProduct;
                productReference.count = countProduct;
            });

            IconMin.addEventListener('click', (event) => {
                event.preventDefault();
                if (countProduct > 0) countProduct--;
                count.innerHTML = countProduct;
                productReference.count = countProduct;
            });
        }

        const formName = document.getElementById('form-name');
        const sub = productList.querySelector('.confirmListProduct');
        sub.addEventListener('click', async (event) => {
            event.preventDefault();
            let parcelName = {};
            const formData = new FormData(formName);
            for (const [key, value] of formData.entries()) parcelName[key] = value;

            fetch(`http://127.0.0.1:8000/parcel/add_parcel/?name=${parcelName['name']}&last_name=${parcelName['last_name']}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ data: addParcel })
            })
                .then(res => res.json())
                .then(data => console.log('✅ ثبت مرسوله:', data))
                .catch(err => console.error('❌ خطا در ثبت مرسوله:', err));
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
