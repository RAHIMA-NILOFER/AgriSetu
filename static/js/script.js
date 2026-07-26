// ==========================================================
// AGRISETU
// MAIN JAVASCRIPT
// ==========================================================

document.addEventListener("DOMContentLoaded", function () {

    // ==========================================
    // AUTO CLOSE ALERTS
    // ==========================================

    setTimeout(function () {

        document.querySelectorAll(".alert").forEach(function (alert) {

            let bsAlert = bootstrap.Alert.getOrCreateInstance(alert);

            bsAlert.close();

        });

    }, 4000);


    // ==========================================
    // TOOLTIPS
    // ==========================================

    var tooltipTriggerList = [].slice.call(

        document.querySelectorAll('[data-bs-toggle="tooltip"]')

    );

    tooltipTriggerList.map(function (tooltipTriggerEl) {

        return new bootstrap.Tooltip(tooltipTriggerEl);

    });


    // ==========================================
    // CONFIRM DELETE
    // ==========================================

    document.querySelectorAll(".delete-btn").forEach(function(btn){

        btn.addEventListener("click",function(e){

            if(!confirm("Are you sure you want to delete this farmer?")){

                e.preventDefault();

            }

        });

    });


    // ==========================================
    // FARMER SEARCH
    // ==========================================

    let farmerSearch=document.getElementById("farmerSearch");

    if(farmerSearch){

        farmerSearch.addEventListener("keyup",function(){

            let value=this.value.toLowerCase();

            let rows=document.querySelectorAll("#farmersTable tbody tr");

            rows.forEach(function(row){

                if(row.innerText.toLowerCase().includes(value)){

                    row.style.display="";

                }

                else{

                    row.style.display="none";

                }

            });

        });

    }


    // ==========================================
    // HISTORY SEARCH
    // ==========================================

    let historySearch=document.getElementById("historySearch");

    if(historySearch){

        historySearch.addEventListener("keyup",function(){

            let value=this.value.toLowerCase();

            let rows=document.querySelectorAll("#historyTable tbody tr");

            rows.forEach(function(row){

                if(row.innerText.toLowerCase().includes(value)){

                    row.style.display="";

                }

                else{

                    row.style.display="none";

                }

            });

        });

    }


    // ==========================================
    // INVENTORY SEARCH
    // ==========================================

    let inventorySearch=document.getElementById("inventorySearch");

    if(inventorySearch){

        inventorySearch.addEventListener("keyup",function(){

            let value=this.value.toLowerCase();

            let rows=document.querySelectorAll("#inventoryTable tbody tr");

            rows.forEach(function(row){

                if(row.innerText.toLowerCase().includes(value)){

                    row.style.display="";

                }

                else{

                    row.style.display="none";

                }

            });

        });

    }


    // ==========================================
    // LIVE CLOCK
    // ==========================================

    let clock=document.getElementById("liveClock");

    if(clock){

        setInterval(function(){

            let now=new Date();

            clock.innerHTML=now.toLocaleString();

        },1000);

    }


    // ==========================================
    // COUNTER ANIMATION
    // ==========================================

    document.querySelectorAll(".counter").forEach(function(counter){

        let target=parseInt(counter.innerText);

        if(isNaN(target)) return;

        let count=0;

        let increment=Math.max(1,Math.ceil(target/100));

        counter.innerText=0;

        let timer=setInterval(function(){

            count+=increment;

            if(count>=target){

                counter.innerText=target;

                clearInterval(timer);

            }

            else{

                counter.innerText=count;

            }

        },15);

    });


    // ==========================================
    // BACK TO TOP BUTTON
    // ==========================================

    let topButton=document.getElementById("topBtn");

    if(topButton){

        window.addEventListener("scroll",function(){

            if(window.scrollY>250){

                topButton.style.display="block";

            }

            else{

                topButton.style.display="none";

            }

        });

        topButton.addEventListener("click",function(){

            window.scrollTo({

                top:0,

                behavior:"smooth"

            });

        });

    }


    // ==========================================
    // FADE-IN ANIMATION
    // ==========================================

    let observer=new IntersectionObserver(function(entries){

        entries.forEach(function(entry){

            if(entry.isIntersecting){

                entry.target.classList.add("show");

            }

        });

    });

    document.querySelectorAll(".fade-card").forEach(function(card){

        observer.observe(card);

    });


    // ==========================================
    // REGISTER FORM VALIDATION
    // ==========================================

    let registerForm=document.querySelector("form");

    if(registerForm){

        registerForm.addEventListener("submit",function(e){

            let mobile=document.querySelector("input[name='mobile']");

            if(mobile){

                if(mobile.value.length!==10){

                    alert("Mobile number must contain exactly 10 digits.");

                    e.preventDefault();

                    return;

                }

            }

        });

    }

});