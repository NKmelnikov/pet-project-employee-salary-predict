$(document).ready(function () {

    const a = {
        select_department: $('#id_department'),
        select_jobtitle: $('#id_jobtitle'),
        name: $('#name'),
        hire_date: $('#hire_date'),
        annual_rt: $('#annual_rt'),
        datepicker: $("#datetimepicker1"),
        post_form: $('#post-form'),
        btn_migrate: $('#btn_migrate'),
        option: $("<option></option>"),
        modal_prediction: $('#exampleModal'),

        clear_jobtitle_options() {
            a.select_jobtitle.empty();
            a.select_jobtitle.append($("<option></option>")
                .attr("value", "").text('--------------'));
        },

        get_jobtitle_options(_this) {
            a.clear_jobtitle_options()
            a.select_jobtitle.prop('disabled', false);
            $.get(`/jobtitles/${_this.value}`, function (data) {
                $.each(data, function (key, value) {
                    a.select_jobtitle.append($("<option></option>")
                        .attr("value", value.id).text(value.name));
                });
            })
        },

        validate_inputs() {
            const condition =
                a.name.val().length === 0 ||
                a.annual_rt.val().length === 0 ||
                $('#id_department option:selected').text() === '--------------' ||
                $('#id_jobtitle option:selected').text() === '--------------'

            if (condition) {
                alert('Please select department and job title')
                return false;
            }

            return true;
        },

        makePrediction() {
            $.ajax({
                type: 'POST',
                url: '/predict/',
                data: {
                    name: a.name.val(),
                    department: $('#id_department option:selected').text(),
                    jobtitle: $('#id_jobtitle option:selected').text(),
                    hire_date: a.hire_date.val(),
                    annual_rt: a.annual_rt.val(),
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                    action: 'post'
                },
                success: function (json) {
                    document.getElementById("prediction").innerHTML = json['result']
                    document.getElementById("we").innerHTML = json['work_exp']
                    document.getElementById("di").innerHTML = json['department']
                },
                error: function (xhr, errmsg, err) {

                }
            });
        },

        get_prediction(e) {
            e.preventDefault();
            if (a.validate_inputs()) {
                a.modal_prediction.modal('show');
                a.makePrediction()
            }
        },

        perform_migration() {
            $.ajax({
                type: 'GET',
                url: '/migrate/',
                success: function (json) {
                    if (json.message === 'success') {
                        alert('Data was successfully migrated');
                        location.reload();
                    }
                },
                error: function (xhr, errmsg, err) {
                    alert(xhr.responseText);
                    console.log(errmsg);
                    console.log(err);
                }
            });

        }

    }

    a.post_form.on('submit', (e) => {
        a.get_prediction(e);
    });

    a.btn_migrate.on('click', () => {
        a.perform_migration();
    });

    a.select_jobtitle.prop('disabled', true);
    a.select_department.on('change', function () {
        a.get_jobtitle_options(this)
    });

    if (a.datepicker.parents('html').length > 0) {
        a.datepicker.datetimepicker({
            format: 'YYYY-MM-DD',
            useCurrent: false,
            defaultDate: new Date('1961-04-12'),
            minDate: new Date('1961-04-12'),
            maxDate: new Date('2020-01-01'),
        });
    }
})


