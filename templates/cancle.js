
var div = document.getElementById('cancel-parcel')
var form_cancel_parcel = document.getElementById('cancle-form') // نام فرم کنسل اصلی
var form_name_cancel = document.getElementById('get_name') // نام فرم نام و نام خانوادگی
var subcancleParcel = div.querySelector('.submit-cancel-parcel')

subcancleParcel.addEventListener('click', async (event) => {
    event.preventDefault()
    var show_detail = document.getElementById('show_detail')
    show_detail.innerHTML = ''; // پاک کردن محتوای قبلی قبل از ارسال درخواست جدید

    // اصلاح شده: استفاده از نام‌های صحیح متغیرها
    var formData = new FormData(form_cancel_parcel) 
    var formName = new FormData(form_name_cancel) 

    var parcel = {}
    for (var [key, value] of formData.entries()) {
        parcel[key] = value
    }
    var parcelName = {}
    for (var [key, value] of formName.entries()) {
        parcelName[key] = value
    }
    
    // استفاده از fetch به روش بهتر با async/await
    try {
        const url = `http://127.0.0.1:8000/parcel/parcel/?parcel_id=${parcel['parcel_id']}&name=${parcelName['name']}&last_name=${parcelName['last_name']}`;
        const res = await fetch(url);
        const data = await res.json();

        if (res.status === 404) {
            show_detail.innerHTML = '❌ همچین سفارشی یافت نشد';
            return;
        } 
        
        // مدیریت سایر کدهای خطای غیر از 404 (مثل 500)
        if (!res.ok) {
            // فرض می‌کنیم در صورت خطا، سرور یک پیام خطا در body برمی‌گرداند 
            const errorMessage = data.detail || `خطا در سرور با کد: ${res.status}`;
            show_detail.innerHTML = `⚠️ ${errorMessage}`;
            return;
        }

        // اگر res.ok درست بود و وضعیت 200 بود، نمایش جزئیات:
        
        // نمایش جزئیات بسته
        const details = [
            { label: 'قیمت', value: data.price },
            { label: 'نام محصول', value: data.nameProduct },
            { label: 'مجموع کل', value: data.TotalPrice },
            { label: 'تعداد', value: data.count },
            { label: 'وضعیت', value: data.status },
            { label: 'مبدا', value: data.origin }
        ];

        details.forEach(item => {
            var divDetail = document.createElement('div');
            // بهتر است label و value را جداگانه نمایش دهید
            divDetail.innerHTML = `<strong>${item.label}:</strong> ${item.value}`;
            divDetail.className = 'd-flex flex-column border border-black p-2 mb-1';
            show_detail.appendChild(divDetail);
        });

    } catch (error) {
        // مدیریت خطاهای شبکه (Network Errors)
        console.error('Fetch Error:', error);
        show_detail.innerHTML = '🚨 خطای شبکه: امکان اتصال به سرور وجود ندارد.';
    }
})
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