// 💡 متغیر سراسری برای نگهداری آیدی‌های انتخابی
let selectedParcelIdss = []; 

// ارجاع به المان‌های DOM در خارج از Listenerها
var formsVendors = document.getElementById('chekckListVendor');
var form_vendors = document.getElementById('checkParcel');
var submit_name_vendors = document.querySelector('.send-name');
var showParcelDiv = document.getElementById('show-parcel-check');
var confirmProDiv = document.getElementById('showList'); // یا confrim-pro اگر در جای دیگری استفاده شده
var timeCheckForm = document.getElementById('form-parcel-check');
const sendNumButton = timeCheckForm.querySelector('#send-num');


// --- ۱. تابع مدیریت نمایش دکمه تأیید (اصلاح شده برای URL استاندارد FastAPI) ---
function updateConfirmationArea() {
    
    // ارجاع صحیح به المان
    let choice_product = document.getElementById('showList'); 
    choice_product.innerHTML = ''; // پاک کردن محتوای قبلی

    // مدیریت نمایش فرم زمان‌سنجی
    if (timeCheckForm) {
        if (selectedParcelIdss.length > 0) {
            timeCheckForm.style.display = 'flex';
        } else {
            timeCheckForm.style.display = 'none';
        }
    }

    if (selectedParcelIdss.length > 0) {
        
        // 1. نمایش IDهای انتخاب شده
        let info_div = document.createElement('div');
        info_div.innerHTML = `
            <strong>${selectedParcelIdss.length} سفارش انتخاب شده:</strong> 
            <span>${selectedParcelIdss.join(', ')}</span>
        `;
        info_div.className = 'alert alert-info d-flex gap-3 justify-content-between align-items-center';
        choice_product.appendChild(info_div);

        // 2. ساخت دکمه Confirm 
        let button_send_confrim = document.createElement('button');
        let text_button = document.createTextNode(`تأیید ${selectedParcelIdss.length} سفارش`);
        button_send_confrim.appendChild(text_button);
        button_send_confrim.className = 'btn btn-success mt-2';
        button_send_confrim.style.width = "200px";
        button_send_confrim.style.height = "50px";
        button_send_confrim.style.cursor = "pointer";
        choice_product.appendChild(button_send_confrim);

        // 3. اتصال Listener نهایی به دکمه
        button_send_confrim.addEventListener('click', async () => {
            
            // 🛠️ FIX 1: حذف IDهای تکراری از آرایه انتخابی
            const uniqueIds = [...new Set(selectedParcelIdss)];
            
            const serverIP = 'http://127.0.0.1:8000/parcel';
            
            // 🛠️ FIX 2: ساخت URL به روش استاندارد FastAPI (parcel_id=3&parcel_id=4)
            const urlParams = uniqueIds.map(id => `parcel_id=${id}`).join('&');

            const url = `${serverIP}/submit/?${urlParams}`;

            try {
                const response = await fetch(url);
                if (!response.ok) {
                    let errorData = await response.json();
                    let errorDetail = errorData.detail || `HTTP error! status: ${response.status}`;
                    throw new Error(errorDetail);
                }
                const result = await response.json();
                alert(`سفارشات ID ${uniqueIds.join(', ')} با موفقیت تایید شدند.`);

                // پس از موفقیت، آرایه را خالی و UI را به‌روزرسانی کنید
                selectedParcelIdss = [];
                updateConfirmationArea(); 

            } catch (error) {
                console.error("خطا در تأیید سفارش:", error);
                alert(`خطا در تأیید سفارش: ${error.message}`);
            }
        });
    }
}


// --- ۲. Listener اصلی برای واکشی و نمایش سفارشات ---
submit_name_vendors.addEventListener('click', async (event) => {
    event.preventDefault()
    
    showParcelDiv.innerHTML = '';
    selectedParcelIdss = []; 
    updateConfirmationArea(); // پاکسازی دکمه‌ها و فرم‌های اضافی

    var formData = new FormData(form_vendors)
    var infoVendors = {}

    for (var [key, value] of formData.entries()) {
        infoVendors[key] = value
    }

    try {
        const res = await fetch(`http://127.0.0.1:8000/parcel/parcel-vendor/?name=${infoVendors['name']}&last_name=${infoVendors['last_name']}`);
        
        if (!res.ok) {
            throw new Error(`خطا در واکشی داده‌ها با کد: ${res.status}`);
        }
        
        const data = await res.json();
        
        if (data.length === 0) {
            showParcelDiv.innerHTML = '<div class="alert alert-warning w-100">سفارشی برای این غرفه‌دار یافت نشد.</div>';
            return;
        }

        // ایجاد هدر
        const headerContainer = document.createElement('div');
        headerContainer.className = 'row d-flex border-bottom border-black w-100 mb-2 font-weight-bold text-center';
        headerContainer.innerHTML = `<div class="col-2"><strong>ID</strong></div><div class="col-2"><strong>محصول</strong></div><div class="col-2"><strong>قیمت</strong></div><div class="col-2"><strong>قیمت کل</strong></div><div class="col-2"><strong>وضعیت</strong></div><div class="col-2"><strong>تعداد</strong></div>`;
        showParcelDiv.appendChild(headerContainer);


        // --- ایجاد المنت‌ها برای هر سفارش و Listener انتخاب ---
        for (let i = 0; i < data.length; i++) {
            
            const parcelIdToSelect = data[i].id;
            
            const parcelContainer = document.createElement('div');
            parcelContainer.className = 'row d-flex border border-black w-100 mb-2 align-items-center text-center';
            parcelContainer.style.cursor = "pointer"; 

            parcelContainer.innerHTML = `
                <div class="col-2 show_id"><strong>${parcelIdToSelect}</strong></div>
                <div class="col-2">${data[i].nameProduct}</div>
                <div class="col-2">${data[i].price}</div>
                <div class="col-2">${data[i].TotalPrice}</div>
                <div class="col-2">${data[i].status}</div>
                <div class="col-2">${data[i].count}</div>
            `;
            
            showParcelDiv.appendChild(parcelContainer);
            
            // 🛠️ FIX 3: Listener انتخاب روی کل Container اعمال می‌شود و logic کاملاً صحیح است.
            parcelContainer.addEventListener('click', (event) => {
                event.preventDefault();
                
                const index = selectedParcelIdss.indexOf(parcelIdToSelect);

                if (index !== -1) {
                    // حذف آیتم
                    selectedParcelIdss.splice(index, 1);
                    parcelContainer.style.backgroundColor = "transparent";
                    parcelContainer.style.border = "1px solid black";
                } else {
                    // افزودن آیتم
                    selectedParcelIdss.push(parcelIdToSelect);
                    parcelContainer.style.backgroundColor = "#e0f7fa"; 
                    parcelContainer.style.border = "3px solid #00bcd4";
                }

                updateConfirmationArea(); 
            });
        }
        
    } catch (error) {
        console.error("خطا در واکشی سفارشات:", error);
        showParcelDiv.innerHTML = `<div class="alert alert-danger w-100">خطا در ارتباط با سرور یا واکشی: ${error.message}</div>`;
    }
});


// --- ۳. Listener ارسال زمان (برای چک کردن زمان تایید) ---
// 🛠️ FIX 4: این Listener یک بار در هنگام بارگذاری اسکریپت تعریف می‌شود و از تکرار Listener جلوگیری می‌کند.
sendNumButton.addEventListener('click', async (event) => {
    event.preventDefault();

    // استفاده از اولین ID انتخاب شده (اگر چند ID انتخاب شده باشند)
    const parcelIdToSend = selectedParcelIdss.length > 0 ? selectedParcelIdss[0] : null;

    if (!parcelIdToSend) {
        alert("لطفاً یک سفارش را برای ارسال زمان انتخاب کنید.");
        return;
    }

    // گرفتن مقدار input
    const timeValue = document.querySelector('#form-parcel-check input[name="number"]').value;

    if (!timeValue || isNaN(parseInt(timeValue))) {
        alert("لطفاً یک عدد معتبر برای زمان وارد کنید.");
        return;
    }

    const serverIP = 'http://127.0.0.1:8000';
    // 🛠️ FIX 5: اصلاح URL برای check_parcel_time
    const destinationUrl = `${serverIP}/parcel/check_parcel_time/?parcel_id=${parcelIdToSend}&time_value=${timeValue}`;

    try {
        const response = await fetch(destinationUrl);

        let result = {};
        try {
            result = await response.json();
        } catch (e) { /* اگر پاسخ json نبود، اشکالی ندارد */ }

        if (!response.ok) {
            throw new Error(result.detail || `خطا در سرور با کد: ${response.status}`);
        }

        alert(`زمان‌سنجی برای سفارش ID ${parcelIdToSend} با موفقیت ارسال شد.`);
    } catch (error) {
        console.error("خطا در ارسال زمان:", error);
        alert(`خطا: ${error.message}`);
    }
});