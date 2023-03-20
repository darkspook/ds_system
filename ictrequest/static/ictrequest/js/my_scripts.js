//Confirm Modal
$('#myform').submit(function(e) {
	e.preventDefault(); // prevent the form from submitting

    $('#confirm-submit-modal').modal('show'); // display the confirmation modal
});

$('#confirm-submit-btn').click(function() {
    $('#myform').off('submit'); // remove the submit event handler to avoid an infinite loop
    $('#myform').submit(); // submit the form
});

// Tree
$(function () {
	$('.tree li:has(ul)').addClass('parent_li').find(' > span').attr('title', 'Collapse this branch');
	
	// if($('.tree ul').has("li").length > 0) {
	// 	//$('.fa-plus-square').attr('style', 'display: none;');
	// 	$(this).css("background", "#ff0000");
	// 	$('.tree li:has(ul)').addClass('parent_li').find(' > i')attr('title', 'test');
	// } 

	$('.tree li.parent_li > span').on('click', function (e) {
		var children = $(this).parent('li.parent_li').find(' > ul > li');
		if (children.is(":visible")) {
			children.hide('fast');
			$(this).attr('title', 'Expand this branch').find(' > i').addClass('fa-plus-square').removeClass('fa-minus-square');
		} else {
			children.show('fast');
			$(this).attr('title', 'Collapse this branch').find(' > i').addClass('fa-minus-square').removeClass('fa-plus-square');
  		}
  		e.stopPropagation();
	});
});

// Topover
$(function () {
	$('.popover-dismiss').popover({
		trigger: 'focus'
	});
});

// SB Admmin Navigation
window.addEventListener('DOMContentLoaded', event => {

    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // Uncomment Below to persist sidebar toggle between refreshes
        // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
        //     document.body.classList.toggle('sb-sidenav-toggled');
        // }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }

});

//Datepicker for new/update asset, new/update component
$(function() {
    $("#id_date_acquired").datepicker({dateFormat:"yy-mm-dd"})
});

//Datepicker for reports
$(function() {
    $("#dateFrom").datepicker({dateFormat:"yy-mm-dd"})
    
    $("#dateTo").datepicker({dateFormat:"yy-mm-dd"})
});
