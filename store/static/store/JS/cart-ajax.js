document.addEventListener("DOMContentLoaded", function () {
  const forms = document.querySelectorAll(".add-to-cart-form");

  forms.forEach((form) => {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      const url = form.action;
      const csrftoken = form.querySelector('[name=csrfmiddlewaretoken]').value;
      const productName = form.dataset.productName;

      fetch(url, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrftoken,
          "X-Requested-With": "XMLHttpRequest",
        },
      }).then((response) => {
        if (response.ok) {
          showToast(`${productName} добавлен в корзину`);
        } else {
          showToast("Ошибка при добавлении в корзину");
        }
      });
    });
  });

  function showToast(message) {
    let toast = document.createElement("div");
    toast.className = "toast-message";
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 2500);
  }
});
