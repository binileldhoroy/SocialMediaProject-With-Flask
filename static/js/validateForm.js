$(function(){
    //login form validation
    $("#loginForm").validate()

    //registration form validation
    $("#registerForm").validate({
        rules:{
            name : {
                required: true,
                nameValidation : true,
            },
            phone : {
                required : true,
                minlength : 10,
                maxlength : 10,
                digits : true,
                phoneNumberValidation : true,
            },
            email : {
                required : true,
                email : true,
            },
            pword : {
                required : true,
                minlength : 6,
            },
            cpword : {
                required : true,
                equalTo : "#pword",
            }
        }
    })

    //post form validation
    $("#postForm").validate({
        rules:{
            desc:{
                required : true,
            },
            image:{
                required : true,
            }
        }
    })

    //additional validation methods

    //for phone number -- must start with 7,8 or 9
    jQuery.validator.addMethod("phoneNumberValidation", function(phone_number, element) {
        phone_number = phone_number.replace(/\s+/g, ""); 
        return this.optional(element) || phone_number.match(/^9\d{8,}$/) || phone_number.match(/^8\d{8,}$/) || phone_number.match(/^7\d{8,}$/);
    }, "Phone number not valid");

    //for name -- must only include letters and spaces
    jQuery.validator.addMethod("nameValidation",function(name,element){
        return this.optional(element) || name.match(/^[A-Za-z\s]+$/);
    }, "Enter a valid name")

    //additional validation methods
})