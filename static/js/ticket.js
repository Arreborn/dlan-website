// most of the functions right below this are very basic JS DOM manipulation, so I won't elaborate on these
// the interesting functions start at line 74
var sum1 = 0;
var sum2 = 0;

function DisplaySum(sum_1, sum_2) {
    total = sum_1 + sum_2;
    if (total > 0) {
    document.getElementById("sum_total").innerHTML =
        "Totalt att betala: " + total;
    }
}

var enableSecondTicket = document.getElementById("enable_second_ticket");
var mainTicketSelect = document.getElementById("main_ticket");
var phoneNo1Collapse = new bootstrap.Collapse(
    document.getElementById("phone_no_1"),
    {
    toggle: false, // disables the automatic collapsing behavior
    }
);

enableSecondTicket.addEventListener("change", function () {
    if (!enableSecondTicket.checked) {
    sum2 = 0;
    DisplaySum();
    }
});

phoneNo1Collapse.hide(); // manually hide the element on load

mainTicketSelect.addEventListener("change", function () {
    if (mainTicketSelect.value == "2") {
    phoneNo1Collapse.show();
    sum1 = 140;
    } else if (mainTicketSelect.value == "1") {
    phoneNo1Collapse.hide();
    sum1 = 90;
    }
    DisplaySum(sum1, sum2);
});

var secondTicketSelect = document.getElementById("secondary_ticket");
var phoneNo2Collapse = new bootstrap.Collapse(
    document.getElementById("phone_no_2"),
    {
    toggle: false, // disables the automatic collapsing behavior
    }
);

phoneNo2Collapse.hide(); // manually hide the element on load

secondTicketSelect.addEventListener("change", function () {
    if (secondTicketSelect.value == "2") {
    phoneNo2Collapse.show();
    sum2 = 140;
    } else if (secondTicketSelect.value == "1") {
    phoneNo2Collapse.hide();
    sum2 = 90;
    }
    DisplaySum(sum1, sum2);
});

var gdprCheck = document.getElementById('gdpr_check');

gdprCheck.addEventListener("change", function () {
    if (gdprCheck.checked) {
        document.getElementById('checkout_button').classList.remove('disabled')
    } else {
        document.getElementById('checkout_button').classList.add('disabled')
    }
})

/* START OF FORM VALIDATION AND REDIRECT FUNCTIONS */

// used to validate all fields in the form
function validateField(fieldId, tagId, validationFunction = (input) => !!input.value) {
  const field = document.getElementById(fieldId);
  const tag = document.getElementById(tagId);
  const isValid = validationFunction(field);
  
  // adds borders to failed fields
  if (isValid) {
    field.classList.remove('border', 'border-danger');
    tag.classList.remove('border', 'border-danger');
  } else {
    field.classList.add('border', 'border-danger');
    tag.classList.add('border', 'border-danger');
  }

  return isValid;
}

// handles double first names by removing spaces or dashes and taking the second part
function handleDoubleFirstName(fname) {
  const nameParts = fname.split(/[-\s]/);
  if (nameParts.length > 1) {
    return nameParts[0];
  }
  return fname;
}

// replaces special characters with their corresponding substitutions
function replaceSpecialChars(name) {
  return name.replace(/[åäÅÄ]/g, 'a').replace(/[öÖ]/g, 'o');
}

// verifies that the submitted liuid matches the first and last name in the form
function validateLiuidFormat(liuid, fname, lname) {
  fname = handleDoubleFirstName(fname);
  lname = replaceSpecialChars(lname);
  fname = replaceSpecialChars(fname);

  const namePart = (fname.slice(0, Math.min(3, fname.length)).toLowerCase() + lname.slice(0, 2).toLowerCase());
  const regex = new RegExp('^' + namePart + '\\d{3}$', 'i');
  return regex.test(liuid);
}



// this function makes an AJAX request to fetch stored liu-ids from the database
async function isLiuidUnique(liuid) {
  const response = await fetch(`/check_liuid_exists/?liuid=${liuid}`);
  const data = await response.json();
  return !data.exists;
}

// this function shows an error message if any field is incorrectly filled out
function showModal(errorMessages) {
  const modalElement = document.getElementById('validation_error');
  const errorBodyElement = document.getElementById('error_body');
  
  // Build the error message string
  const errorMessageString = errorMessages.join('');
  var fullErrorInnerHTML = "<ul>" + errorMessageString + "</ul>"
  errorBodyElement.innerHTML = fullErrorInnerHTML;

  // Show the modal
  const modalInstance = new bootstrap.Modal(modalElement);
  modalInstance.show();
}

// used to compile and return a json object with the complete order
// additinally, validates the entire form and marks the fields with incorrect info as red
// redirects to payment if form is valid, else returns false
async function ValidateForm() {
  const formData = {};
  formData.fname = document.getElementById('fname').value || 'none';
  formData.lname = document.getElementById('lname').value || 'none';
  formData.liuid = document.getElementById('liuid').value || 'none';
  formData.email = document.getElementById('email').value || 'none';
  formData.main_ticket = document.getElementById('main_ticket').value || 'none';
  formData.secondary_ticket = document.getElementById('secondary_ticket').value || 'none';
  formData.groupname = document.getElementById('groupname').value || 'none';
  formData.phone1 = document.getElementById('phone1').value || 'none';
  formData.phone2 = document.getElementById('phone2').value || 'none';

  const isFirstNameValid = validateField('fname', 'fname_tag');
  const isLastNameValid = validateField('lname', 'lname_tag');
  const isLiuidFormatValid = validateField('liuid', 'liuid_tag', (input) => validateLiuidFormat(input.value, formData.fname, formData.lname));
  const isLiuidInDB = await isLiuidUnique(formData.liuid);
  const isEmailValid = validateField('email', 'email_tag');
  const isMainTicketValid = validateField('main_ticket', 'main_ticket_tag', (input) => input.value != 0);
  const isSecondaryTicketValid = document.getElementById('enable_second_ticket').checked
    ? validateField('secondary_ticket', 'secondary_ticket_tag', (input) => input.value != 0)
    : true; // if the secondary ticket is not enabled, it is considered valid

  const isPhone1Valid = formData.main_ticket == 2
    ? validateField('phone1', 'phone1_tag', (input) => !!input.value)
    : true; // if the main ticket is not a plus ticket, phone1 is considered valid

  const isPhone2Valid = document.getElementById('enable_second_ticket').checked && formData.secondary_ticket == 2
    ? validateField('phone2', 'phone2_tag', (input) => !!input.value)
    : true; // if the secondary ticket is not a plus ticket, phone2 is considered valid

  // the legendary boolean
  // pretty much ensures all fields are valid, so we can go on to payment
  const isValid = isFirstNameValid && isLastNameValid && isLiuidFormatValid && isEmailValid && isMainTicketValid && isSecondaryTicketValid && isPhone1Valid && isPhone2Valid && isLiuidInDB;

  // builds a list for error message
  if (isValid) {
    sendFormData(formData)
  } else {
    errorMessages = [];
    if (!isFirstNameValid) {
      errorMessages.push("<li>Du har inte fyllt i något förnamn!</li>");
    }
    if (!isLastNameValid) {
      errorMessages.push("<li>Du har inte fyllt i något efternamn!</li>");
    }
    if (!isLiuidFormatValid) {
      errorMessages.push("<li>Någonting är fel med det LIU-ID du angett!</li>");
    }
    if (!isLiuidInDB && isLiuidFormatValid) {
      errorMessages.push("<li>Detta LIU-ID har redan använts för att boka en biljett!</li>");
    }
    if (!isMainTicketValid) {
      errorMessages.push("<li>Du har inte valt vilken typ av biljett du vill ha!</li>");
    }
    if (!isSecondaryTicketValid) {
      errorMessages.push("<li>Du har angett att du vill köpa två biljetter, men inte angett vad den andra biljetten ska vara!</li>");
    }
    if (!isPhone1Valid) {
      errorMessages.push("<li>Du har angett att du vill beställa datorskjuts till biljett 1, men inte angett ett telefonnummer för denna biljett!</li>");
    }
    if (!isPhone2Valid) {
      errorMessages.push("<li>Du har angett att du vill beställa datorskjuts till biljett 2, men inte angett ett telefonnummer för denna biljett!</li>");
    }
    showModal(errorMessages);
  }
}

// this line kicks off validation, which in turn will kick off payment
document.getElementById('checkout_button').addEventListener("click", ValidateForm);

// this function talks to django, and redirects to the view stripe_checkout in views.py
function sendFormData(formData) {
  const url = '/stripe_checkout/';

  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(formData)
  })
    .then(function (response) {
      return response.json();
    })
    .then(function (session) {
      // use the public key here to authenticate with Stripe

      // public key test
      const stripe = Stripe('pk_test_51K58IHGo0k2FYhZuGUh9Kz0LNfn1i4EsgGvhsl3EUNeXwExd2Q01YAr2smhESQIQv0vjMYBXBPsRKV2nLa3QEWuY00QCKr39fI');

      // public key live
      // const stripe = Stripe('pk_live_51K58IHGo0k2FYhZudoIWYYgNCpqD2wFQ7e69blyhvARI69W4wfouafrclqXbqJX5AQ61G6YSAFdgasrVSbenj2Rm00o4xJYZJC');
      
      // not sure if this error is 100% required, but it feels nice
      // never got it to trigger in testing
      stripe.redirectToCheckout({ sessionId: session.session_id }).then(function (result) {
        console.error(result.error.message);
      });
    })
    // same with this catch, never managed to get it to trigger
    // should be a good sign..?
    .catch(function (error) {
      console.error(error);
    });
}
