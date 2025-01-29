(function($) {
    $(document).ready(function() {
        $('#id_menu_type').change(function() {
            const menuType = $(this).val();

            if (menuType === 'detail') {
                $('#id_linked_model').closest('.form-row').show();
                $('#id_linked_object').closest('.form-row').show();
            } else if (menuType === 'list') {
                $('#id_linked_model').closest('.form-row').show();
                $('#id_linked_object').closest('.form-row').hide();
            } else {
                $('#id_linked_model').closest('.form-row').hide();
                $('#id_linked_object').closest('.form-row').hide();
            }
        });

        $('#id_linked_model').change(function() {
            const modelName = $(this).val();
            const objectSelect = $('#id_linked_object');

            if (modelName) {
                $.ajax({
                    url: '/admin/get_objects/', // Dinamik obyektlarni yuklash URL
                    data: {
                        model: modelName,
                    },
                    success: function(data) {
                        objectSelect.html('<option value="">--- Obyekt tanlang ---</option>');
                        $.each(data.objects, function(index, object) {
                            objectSelect.append(`<option value="${object.id}">${object.name}</option>`);
                        });
                    }
                });
            } else {
                objectSelect.html('<option value="">--- Obyekt tanlang ---</option>');
            }
        });

        $('#id_menu_type').trigger('change');
    });
})(django.jQuery);
