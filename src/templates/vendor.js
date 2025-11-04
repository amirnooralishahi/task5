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
    choice_product.className='d-flex justify-content-center align-items-center'
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

            const url = `${serverIP}/check_parcel_expire/?${urlParams}`;

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

        let showing = document.getElementById('showing')
            showing.className= 'row d-flex justify-content-center  border border-black w-100 gap-2'
        let parcelIdToSelect=[]
        let number = 0
        for (let i = 0; i <data.id.length; i++) {

            
             let parcelContainer = document.createElement('div');
            parcelContainer.className= 'row d-flex justify-content-center  border border-black w-100 gap-2'
            parcelContainer.style.cursor = "pointer"; 
            
            
            let divId= document.createElement('div')
            divId.innerHTML = data.id[i] 
            divId.className= ' d-flex flex-column align-items-center text-center'
            parcelContainer.appendChild(divId)
            number = data.id

            let divName = document.createElement('div')
            divName.innerHTML=data.nameProduct[i]
            divName.className= 'd-flex flex-column align-items-center border border-black'            
            parcelContainer.appendChild(divName)

            let divPrice = document.createElement('div')
            divPrice.innerHTML= data.price[i]
            divPrice.className= ' d-flex flex-column align-items-center border border-black'            

            parcelContainer.appendChild(divPrice)

            
            let divTotal = document.createElement('div')
            divTotal.innerHTML =data.TotalPrice[i]
            divTotal.className= ' d-flex flex-column align-items-center border border-black'            

            parcelContainer.appendChild(divTotal)

            let divStatus = document.createElement('div')
            divStatus.innerHTML= data.status[i] 
            divStatus.className= ' d-flex flex-column align-items-center border border-black'            

            parcelContainer.appendChild(divStatus)

            let divCount = document.createElement('div')
            divCount.innerHTML= data.count[i] 
            divCount.className= ' d-flex flex-column align-items-center border border-black'            
            parcelContainer.appendChild(divCount)
            
            
            
            showing.appendChild(parcelContainer)
            parcelContainer.addEventListener('click', (event) => {
                event.preventDefault();
                parcelIdToSelect.push(data.id[i])
                
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
    const destinationUrl = `${serverIP}/parcel/check_parcel_expire/?time=${timeValue}&parcel_id=${parcelIdToSend}`;

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



//add product to basket product  
                let listShowAdd=document.getElementById('listShowAdd') 

let form_product=document.getElementById('form-product')
let productView= document.getElementById('productView')
let subProduct = productView.querySelector('.sendInfo')
subProduct.addEventListener('click',async (event)=>{
    event.preventDefault()
    let dataProduct =new FormData(form_product)
    let parcel ={}
    let addProduct = {}
    for (var [key,value] of dataProduct.entries()){
        parcel[key]=value
        
    }
    
    try{
        fetch(`http://127.0.0.1:8000/parcel/add-product-by-vendor/?name=${parcel['name']}&last_name=${parcel['last_name']}`,{
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({parcel})
            }).then(res =>{ 
                
            return res.json()}).then(data=>{

                for (let i =0 ;i<Object.keys(data).length  ; i++){ 

                    let divPrice = document.createElement('div')
                    divPrice.innerHTML= data.price
                    divPrice.className='col-4' 
                    let count = document.createElement('div')
                    count.innerHTML = data.count
                    count.className='col-4' 
                    
                    let divName = document.createElement('div')
                    divName.innerHTML = data.name_product
                    divName.className='col-4' 
                    
                    listShowAdd.appendChild(divName)
                    listShowAdd.appendChild(divPrice)
                    listShowAdd.appendChild(count)
                    listShowAdd.className= 'row d-flex gap-4'
                    
                }
                

             }).catch(err => console.error(err))
    }catch{}
})
