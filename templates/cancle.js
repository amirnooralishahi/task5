var div = document.getElementById('cancel-parcel')
var subcancleParcel = div.querySelector('.submit-cancel-parcel')

var form_cancel_parcel = document.getElementById('cancle-form-parcel')
var form_name_cancel = document.getElementById('get_name')

subcancleParcel.addEventListener('click', async (event) => {
    event.preventDefault()
    var show_detail = document.getElementById('show_detail')
    show_detail.innerHTML = '';

    var formData = new FormData(form_cancel_parcel)
    var formName = new FormData(form_name_cancel)

    var parcel = Object.fromEntries(formData.entries())
    var parcelName = Object.fromEntries(formName.entries())

    try {
        const url = `http://127.0.0.1:8000/parcel/parcel/?parcel_id=${parcel['parcel_id']}&name=${parcelName['name']}&last_name=${parcelName['last_name']}`;


        let data = {};
        const res = await fetch(url);
        data = await res.json();
        console.log(res.status);
    
    
        const details = [
            { label: 'قیمت', value: data['price'] },
            { label: 'نام محصول', value: data.nameProduct },
            { label: 'مجموع کل', value: data.TotalPrice },
            { label: 'تعداد', value: data.count },
            { label: 'وضعیت', value: data.status },
            { label: 'مبدا', value: data.origin }
        ];

        details.forEach(item => {
            var divDetail = document.createElement('div');
            divDetail.innerHTML = `<strong>${item.label}:</strong> ${item.value}`;
            divDetail.className = 'd-flex flex-column border border-black p-2 mb-1';
            show_detail.appendChild(divDetail);
        });





        // مدیریت سایر کدهای خطای غیر از 2xx

    } catch (error) {
        console.error('Fetch Error:', error);
        show_detail.innerHTML = '🚨 خطای شبکه: امکان اتصال به سرور وجود ندارد.';
            if (res.status === 404) {
            show_detail.innerHTML = '❌ همچین سفارشی یافت نشد';
            return;
        }
            if (!res.ok) {
            const errorMessage = data.detail || `خطا در سرور با کد: ${res.status}`;
            show_detail.innerHTML = `⚠️ ${errorMessage}`;
            return;
        }
    }
})


var div = document.getElementById('cancel-invoice')
var form_cancel = document.getElementById('cancle-form_invoice')
var form_name = document.getElementById('get_name_invoice')
var subcancle = div.querySelector('.submit-cancel')

subcancle.addEventListener('click', async (event) => {
    event.preventDefault()
    var show_detail = document.getElementById('show_detail_invoice')
    show_detail.innerHTML = '';

    var formData = new FormData(form_cancel)
    var formName = new FormData(form_name)
    var parcel = Object.fromEntries(formData.entries())
    var parcelName = Object.fromEntries(formName.entries())

    fetch(`http://127.0.0.1:8000/parcel/cancel_invoice/?invoice_id=${parcel['invoice_id']}&name=${parcelName['name']}&last_name=${parcelName['last_name']}`)
        .then((res) => {

            if (res.status === 404) {
                show_detail.innerHTML = '❌ همچین سفارشی یافت نشد'
                return res.json().catch(() => ({ detail: 'Not Found' })).then(data => {
                    throw new Error(data.detail || '404 Error');
                });
            }

            if (!res.ok) {
                return res.json().catch(() => ({ detail: `خطا در سرور با کد: ${res.status}` })).then(data => {
                    throw new Error(data.detail || `خطا در سرور با کد: ${res.status}`);
                });
            }

            return res.json();
        })
        .then(data => {
            var divCustomerName = document.createElement('div')
            divCustomerName.innerHTML = `<strong>نام مشتری:</strong> ${data.customer_name}`
            divCustomerName.className = 'd-flex flex-column border border-black p-2'
            show_detail.appendChild(divCustomerName)

            var divInvoiceId = document.createElement('div')
            divInvoiceId.innerHTML = `<strong>شناسه فاکتور:</strong> ${data.invoice_id}`
            divInvoiceId.className = 'd-flex flex-column border border-black p-2'
            show_detail.appendChild(divInvoiceId)

            var divStatus = document.createElement('div')
            divStatus.innerHTML = `<strong>وضعیت:</strong> ${data.status}`
            divStatus.className = 'd-flex flex-column border border-black p-2'
            show_detail.appendChild(divStatus)
        })
        .catch(error => {

            console.error('Fetch Error:', error);
            show_detail.innerHTML = `🚨 ${error.message || 'خطای ناشناخته رخ داده است.'}`;
        });
})