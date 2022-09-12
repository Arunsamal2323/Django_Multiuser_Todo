$(document).ready(function () {
    $("#tag_line").fadeIn("slow");
   
    var upd_task_prev;


    
    function refreshData() {
       
        $.ajax({
            type: 'POST',
            url: '/task/refresh_data/',
            cache: false,
            success: function (data) {
                $('#maintable tbody').find("tr:gt(0)").remove();
                $('#completed-table tbody').find("tr:gt(0)").remove();

                response = JSON.parse(data);

                $('#maintable tbody').find('tr:eq(0)').find('input').val("");

                var dates = []
                for (var i = 0; i < response.length; i++) {
                    dates.push(new Date(response[i].fields['date_posted']));
                }
                var maxDate = new Date(Math.max.apply(null, dates));

                $('.timestamp').text("Last modified on: " + maxDate.toLocaleString('en-US', { month: 'long', day: '2-digit', year: 'numeric' }));

                for (var i = 0; i < response.length; i++) {
                    var task_id = response[i].pk;
                    var task_title = response[i].fields['task_title'];
                    var is_checked = response[i].fields['is_checked'];

                    
                    if (is_checked == false) {
                        var active_row = `<tr class="task_` + task_id + `">
				<td><input type="checkbox" title="Mark as Complete" class="form-check-input mark_as_done"
						id="`+ task_id + `"></td>
				<td colspan="2">
					<h4 class="text-left" id="title'+ task_id +'">` + task_title + `</h4>
				</td>
				<td><i class="fa fa-pencil-square-o update_btns" title="Edit Task" style="color:#0ba8c1;"></i>
					<i class="fa fa-check update_task_btn" title="Update"
						style="color: rgb(16, 172, 211); display: none;"></i>
					<i class="fa fa-close deleterow delete_existing_row" title="Delete Task"
						style="color:red; float:right;"></i>
			</tr>`;
                        $('#maintable tbody').append(active_row);

                    }
                 
                    else {
                        var completed_row = `<tr class="task_` + task_id + `">
                    <td>
    
                        <input type="checkbox" title="Mark as Incomplete" class="form-check-input mark_as_undone"
                            id="`+ task_id + `" checked></td>
                    <td>
                        <h4 class="text-left completed_tasks" id="title`+ task_id + `">` + task_title + `</h4>
                    </td>
                    <td class="button-row"></td>
                </tr>`;
                        $('#completed-table tbody').append(completed_row);

                    }
                }
            }
        });

        
    }

   
    window.setTimeout(function () {
        $(".alert").fadeTo(500, 0).slideUp(500, function () {
            $(this).remove();
        });
    }, 5000);


    
    $(document).on("click", ".update_btns", function () {
        
        upd_task_prev = $(this).parent().parent().find('h4').text().trim();
        var edit_field = '<input type="text" name="task" style="float: left;" class="form-control" id= "add_task" maxlength="60" value="' + upd_task_prev.replace(/"/g, '&quot;') + '" autofocus>';
        $(this).parent().parent().find('td:eq(1)').html(edit_field);
        $(this).hide();
        $(this).siblings('.update_task_btn').show();
    });

    $(document).on("click", ".update_task_btn", function () {
        $(this).hide()
        $(this).siblings('.update_btns').show();
        var upd_task_current = $(this).parent().parent().find('td:eq(1)').find('input').val().trim();
        var upd_id = $(this).parent().parent().find('td:eq(0)').find('input').attr('id');
    
        if (upd_task_current == upd_task_prev && upd_task_current.length > 0) {
            var upd_field = '<h4 class="text-left" id="title' + upd_id + '">' + upd_task_current + '</h4>';
            $('.task_' + upd_id).find('td:eq(1)').html(upd_field);
        }

        else {
            if (upd_task_current.length == 0) {
                alert('Task Name cannot be Empty!');
                var upd_field = '<h4 class="text-left" id="title' + upd_id + '">' + upd_task_prev + '</h4>';
                $('.task_' + upd_id).find('td:eq(1)').html(upd_field);
            }
            else {
                $.ajax({
                    type: 'POST',
                    url: '/task/update_task/',
                    cache: false,
                    data: {
                        task_id: upd_id,
                        task_name: upd_task_current,
                    },
                    success: function () {
                        var upd_field = '<h4 class="text-left" id="title' + upd_id + '">' + upd_task_current + '</h4>';
                        $('.task_' + upd_id).find('td:eq(1)').html(upd_field);

                    }
                });
            }
        }
    });

    $(document).on("click", ".delete_existing_row, .delete_new_row", function () {
        if ($(this).hasClass('delete_new_row')) {
            $(this).parent().parent().remove();
        }
        else {
            var val = $(this).parent().parent().find('input').attr("id");
            var c = confirm('Are you sure you want to delete this task ?');
            if (c == true) {
                $.ajax(
                    {
                        type: "POST",
                        url: "/task/delete_task/",
                        cache: false,
                        data: {
                            task_id: val,
                        },
                        success: function () {
                            refreshData();
                        }
                    });
            }
        }

    });



    $("#completed-table").on('click', '#clear_all_completed_tasks', function () {
    
        if ($('#completed-table tr').length <= 2) {
            alert('No Completed Tasks to Clear!');
        }
        else {
            var cd = confirm('Are you sure you want to delete all completed tasks ?');
            if (cd == true) {
                $.ajax(
                    {
                        type: "POST",
                        url: "/task/delete_all_completed_tasks/",
                        data: {},
                        success: function () {
                            refreshData();
                        }
                    });
            }
        }
    });


    $("table").on('click', "#add_task_btn", function () {
        var task_name;
        task_name = $.trim($('#add_task').val());
        if (task_name != "") {
            
            $.ajax(
                {
                    type: "POST",
                    url: "/task/add_new_task/",
                    data: {
                        task_title: task_name,
                    },
                    
                    success: function (data) 
                    {
                        
                        task_id = data.id;
                        task_name = data.task_title;

                        
                        refreshData();
                    }
                })
        }
        else {
            alert('Enter a Valid Task Name!');
        }
    });


    
    $("table").on('click', ".mark_as_done, .mark_as_undone", function () {
        if ($(this).hasClass('mark_as_done')) {
            var check_id;
            check_id = $(this).attr("id");
            class_name = $(this).attr("class");
            task_name = $("#title" + check_id).html();
            $.ajax(
                {
                    type: "POST",
                    url: "/task/move_tasks/",
                    data: {
                        task_id: check_id,
                        task_class: class_name
                    },
                    success: function () {
                    
                        refreshData();


                    }
                })

        }
        else {
           
            var un_check_id;
            un_check_id = $(this).attr("id");
            task_name = $("#title" + un_check_id).html();
            class_name = $(this).attr("class");
            $.ajax(
                {
                    type: "POST",
                    url: "/task/move_tasks/",
                    data: {
                        task_id: un_check_id,
                        task_class: class_name
                    },
                    success: function () {
                       
                        refreshData();

                    }
                })

        }

    });

});
