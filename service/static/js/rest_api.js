$(function () {
    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#promotion_id").val(res.id);
        $("#promotion_title").val(res.title);
        $("#promotion_code").val(res.promo_code);
        $("#promotion_type").val(res.promo_type);
        $("#promotion_amount").val(res.amount);
        var timestamp = res.start_date;
        var date = new Date(timestamp);
        var formattedDate = date.toISOString().split('T')[0]; // Extract date portion
        $("#promotion_start").val(formattedDate);
        //$("#promotion_start").val(res.start_date);
        var timestamp = res.end_date;
        var date = new Date(timestamp);
        var formattedDate = date.toISOString().split('T')[0]; // Extract date portion
        $("#promotion_end").val(formattedDate); // Set the value of the element with ID "promotion_end" to the extracted date
        //$("#promotion_end").val(res.end_date);
        $("#promotion_is_site_wide").val(res.is_site_wide);

        if (res.is_site_wide == true) {
            $("#promotion_is_site_wide").val("true");
        } else {
            $("#promotion_is_site_wide").val("false");
        }

        $("#promotion_product_id").val(res.product_id);
    }

    function update_search_table(res){
        $("#search_results").empty();
        let table = '<table class="table table-striped" cellpadding="10">'
        table += '<thead><tr>'
        table += '<th class="col-md-2">ID</th>'
        table += '<th class="col-md-2">Title</th>'
        table += '<th class="col-md-2">Code</th>'
        table += '<th class="col-md-2">Type</th>'
        table += '<th class="col-md-2">Amount</th>'
        table += '<th class="col-md-2">Is_Site_Wide</th>'
        table += '<th class="col-md-2">Start</th>'
        table += '<th class="col-md-2">End</th>'
        table += '<th class="col-md-2">Product_id</th>'
        table += '</tr></thead><tbody id="table_content">'
        let firstPromotion = "";
        for(let i = 0; i < res.length; i++) {
            let promotion = res[i];
            table +=  `<tr id="row_${i}"><td>${promotion.id}</td><td>${promotion.title}</td><td>${promotion.promo_code}</td><td>${promotion.promo_type}</td><td>${promotion.amount}</td><td>${promotion.is_site_wide}</td><td>${promotion.start_date}</td><td>${promotion.end_date}</td><td>${promotion.product_id}</td></tr>`;
            if (i == 0) {
                firstPromotion = promotion;
            }
        }
        table += '</tbody></table>';
        $("#search_results").append(table);
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#promotion_title").val("");
        $("#promotion_code").val("");
        $("#promotion_type").val("");
        $("#promotion_amount").val("");
        $("#promotion_is_site_wide").val("");
        $("#promotion_end").val("");
        $("#promotion_start").val("");
        $("#promotion_product_id").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Promotion
    // ****************************************

    $("#create-btn").click(function () {
        let title = $("#promotion_title").val();
        let code = $("#promotion_code").val();
        let type = $("#promotion_type").val();
        let amount = $("#promotion_amount").val();
        let status = $("#promotion_is_site_wide").val() == "true";
        let start = $("#promotion_start").val();
        let end = $("#promotion_end").val();
        let product_id = $("#promotion_product_id").val();

        let data = {
            "title": title,
            "promo_code": code,
            "promo_type": type,
            "amount": amount,
            "is_site_wide": status,
            "start_date": start,
            "end_date": end,
            "product_id": product_id
        };

        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "POST",
            url: "/promotions",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Update a Promotion
    // ****************************************

    $("#update-btn").click(function () {

        let promotion_id = $("#promotion_id").val();
        let title = $("#promotion_title").val();
        let code = $("#promotion_code").val();
        let type = $("#promotion_type").val();
        let amount = $("#promotion_amount").val();
        let status = $("#promotion_is_site_wide").val() == "true";
        let end = $("#promotion_end").val();
        let start = $("#promotion_start").val();
        let product_id = $("#promotion_product_id").val();

        let data = {
            "title": title,
            "promo_code": code,
            "promo_type": type,
            "amount": amount,
            "is_site_wide": status,
            "start_date": start,
            "end_date": end,
            "product_id": product_id
        };

        $("#flash_message").empty();
        let ajax = $.ajax({
                type: "PUT",
                url: `/promotions/${promotion_id}`,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a Promotion
    // ****************************************

    $("#retrieve-btn").click(function () {
        let promotion_id = parseInt($("#promotion_id").val());
        $("#flash_message").empty();
        let ajax = $.ajax({
            type: "GET",
            url: `/promotions/${promotion_id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });
    });

    // ****************************************
    // Delete a Promotion
    // ****************************************

    $("#delete-btn").click(function () {
        let promotion_id = $("#promotion_id").val();
        $("#flash_message").empty();
        let ajax = $.ajax({
            type: "DELETE",
            url: `/promotions/${promotion_id}`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Promotion has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });

    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#promotion_id").val("");
        $("#flash_message").empty();
        clear_form_data()
    });

    // ****************************************
    // Activate a Promotion
    // ****************************************

    $("#activate-btn").click(function () {

        let promotion_id = $("#promotion_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "PUT",
            url: `/promotions/${promotion_id}/activate`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Promotion has been Activated!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // List all promotions
    // ****************************************

    $("#list-btn").click(function () {
        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "GET",
            url: "/promotions",
            contentType: "application/json",
        });
        ajax.done(function(res){
            console.log(res)
            update_search_table(res)
            flash_message("Success")
        });
        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });

    // ****************************************
    // Search for a Promotion
    // ****************************************

    $("#search-btn").click(function () {

        let status = $("#promotion_is_site_wide").val() == "true";
        let title = $("#promotion_title").val();
        let code = $("#promotion_code").val();
        let type = $("#promotion_type").val();

        let queryString = ""

        //queryString += 'status=' + status
        
        if (status){
            queryString += 'status=' + status
        }
        else if (title) {
            if (queryString.length > 0) {
                queryString += '&title=' + title
            } else {
                queryString += 'title=' + title
            }
        }
        else if (code) {
            if (queryString.length > 0) {
                queryString += '&code=' + code
            } else {
                queryString += 'code=' + code
            }
        }
        else if (type) {
            if (queryString.length > 0) {
                queryString += '&type=' + type
            } else {
                queryString += 'type=' + type
            }
        }

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/promotions?${queryString}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())

            update_search_table(res)
            
            // copy the first result to the form
            if (firstPromotion != "") {
                update_form_data(firstPromotion)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    // $("#search-btn").click(function () {

    //     let title = $("#promotion_title").val();
    //     let code = $("#promotion_code").val();
    //     let type = $("#promotion_type").val();
    //     let amount = $("#promotion_amount").val();
    //     let status = $("#promotion_is_site_wide").val();
    //     let end = $("#promotion_end").val();
    //     let start = $("#promotion_start").val();
    //     let product_id = $("#promotion_product_id").val();
        
    //     let queryString = ""
        
    //     if (title) {
    //         queryString += 'title=' + title
    //     }
    //     else if (code) {
    //         if (queryString.length > 0) {
    //             queryString += '&code=' + code
    //         } else {
    //             queryString += 'code=' + code
    //         }
    //     }
    //     else if (type) {
    //         if (queryString.length > 0) {
    //             queryString += '&type=' + type
    //         } else {
    //             queryString += 'type=' + type
    //         }
    //     }
    //     else if (amount) {
    //         if (queryString.length > 0) {
    //             queryString += '&amount=' + amount
    //         } else {
    //             queryString += 'amount=' + amount
    //         }
    //     }
    //     else if (status) {
    //         if (queryString.length > 0) {
    //             queryString += '&status=' + status
    //         } else {
    //             queryString += 'status=' + status
    //         }
    //     }
    //     else if (end) {
    //         if (queryString.length > 0) {
    //             queryString += '&end=' + end
    //         } else {
    //             queryString += 'end=' + end
    //         }
    //     }
    //     else if (start) {
    //         if (queryString.length > 0) {
    //             queryString += '&start=' + start
    //         } else {
    //             queryString += 'start=' + start
    //         }
    //     }
    //     else if (product_id) {
    //         if (queryString.length > 0) {
    //             queryString += '&product_id=' + product_id
    //         } else {
    //             queryString += 'product_id=' + product_id
    //         }
    //     }

    //     $("#flash_message").empty();

    //     let ajax = $.ajax({
    //         type: "GET",
    //         url: `/promotions?${queryString}`,
    //         contentType: "application/json",
    //         data: ''
    //     })

    //     ajax.done(function(res){
    //         //alert(res.toSource())
    //         $("#search_results").empty();
    //         let table = '<table class="table table-striped" cellpadding="10">'
    //         table += '<thead><tr>'
    //         table += '<th class="col-md-2">ID</th>'
    //         table += '<th class="col-md-2">Title</th>'
    //         table += '<th class="col-md-2">Code</th>'
    //         table += '<th class="col-md-2">Type</th>'
    //         table += '<th class="col-md-2">Amount</th>'
    //         table += '<th class="col-md-2">Is_Site_Wide</th>'
    //         table += '<th class="col-md-2">Start</th>'
    //         table += '<th class="col-md-2">End</th>'
    //         table += '<th class="col-md-2">Product_id</th>'
    //         table += '</tr></thead><tbody>'
    //         let firstPromotion = null;
    //         for(let i = 0; i < res.length; i++) {
    //             let promotion = res[i];
    //             table +=  `<tr id="row_${i}"><td>${promotion.id}</td><td>${promotion.title}</td><td>${promotion.promo_code}</td><td>${promotion.promo_type}</td><td>${promotion.amount}</td><td>${promotion.is_site_wide}</td><td>${promotion.start_date}</td><td>${promotion.end_date}</td><td>${promotion.product_id}</td></tr>`;
    //             if (firstPromotion === null) {
    //                 firstPromotion = promotion;
    //             }
    //         }
    //         table += '</tbody></table>';
    //         $("#search_results").append(table);

    //         // copy the first result to the form
    //         if (firstPromotion !== null) {
    //             update_form_data(firstPromotion)
    //         }

    //         flash_message("Success")
    //     });

    //     ajax.fail(function(res){
    //         flash_message(res.responseJSON.message)
    //     });

    });

})
