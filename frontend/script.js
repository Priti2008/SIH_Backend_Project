console.log("JS Connected Successfully");
const loginBtn = document.getElementById("loginBtn");

if (loginBtn) {

    loginBtn.addEventListener("click", () => {

        const email =
        document.getElementById("email").value;

        const password =
        document.getElementById("password").value;

        const validEmail =
        "admin@bordereye.com";

        const validPassword =
        "admin123";

        if(email === "" || password === ""){

            alert(
                "Please enter Email and Password"
            );

            return;
        }

        if(
            email === validEmail &&
            password === validPassword
        ){

            const openDashboard = confirm(
                "Login Successful!\n\nOpen Dashboard?"
            );

            if(openDashboard){

                window.location.href =
                "dashboard.html";
            }

        }else{

            alert(
                "Invalid Email or Password"
            );

        }

    });

}




const signupBtn = document.getElementById("signupBtn");

if (signupBtn) {

    signupBtn.addEventListener("click", () => {

        const name = document.getElementById("name").value;

        const email = document.getElementById("signupEmail").value;

        const password = document.getElementById("signupPassword").value;

        if (
            name === "" ||
            email === "" ||
            password === ""
        ) {

            alert("Please fill all fields");
            return;
        }

        const openDashboard = confirm(
            "Account Created Successfully!\n\nOpen Dashboard?"
        );

        if (openDashboard) {

            window.location.href = "dashboard.html";

        }

    });

}