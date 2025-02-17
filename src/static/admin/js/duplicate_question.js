document.addEventListener("DOMContentLoaded", function() {
    // Функция, которая прикрепляет обработчики клика к кнопкам дублирования
    function attachDuplicateListeners() {
        const questionsContainer = document.querySelector("#questions-group > fieldset");
        buttons.forEach(function(button) {
            // Чтобы не прикреплять несколько обработчиков, можно сначала удалить старый
            button.removeEventListener('click', duplicateHandler);
            button.addEventListener('click', duplicateHandler);
        });
    }

    // Обработчик нажатия кнопки дублирования
    function duplicateHandler(event) {
        event.preventDefault();

        // Находим ближайший контейнер инлайн-формы вопроса.
        // Замените селектор '.dynamic-question_set' на актуальный для вашей страницы.
        var inlineContainer = event.target.closest('.dynamic-question_set');
        if (!inlineContainer) {
            alert("Не удалось найти контейнер формы вопроса.");
            return;
        }

        // Клонируем найденный контейнер
        var clone = inlineContainer.cloneNode(true);

        // Очистим поле идентификатора в клонированной форме (если оно есть)
        var idInputs = clone.querySelectorAll("input[name$='-id']");
        idInputs.forEach(function(input) {
            input.value = "";
        });

        // Обновляем значение TOTAL_FORMS в management form инлайн-форм
        var managementFormInput = inlineContainer.parentNode.querySelector("input[name$='TOTAL_FORMS']");
        if (managementFormInput) {
            var totalForms = parseInt(managementFormInput.value, 10);
            managementFormInput.value = totalForms + 1;
        }

        // Вставляем клон после исходного контейнера
        inlineContainer.parentNode.insertBefore(clone, inlineContainer.nextSibling);

        // При необходимости обновляем индексы полей в клонированной форме
        // (Это может быть нужно, если nested_admin не обновляет их автоматически)

        // Повторно прикрепляем обработчики к кнопкам в новом клоне
        attachDuplicateListeners();
    }

    // Инициализируем обработчики после загрузки страницы
    attachDuplicateListeners();
});
