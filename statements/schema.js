(function() {
			
	Object.prototype.GetSchemaV2 = function(str) {
	
		var obj = {};
		obj = essentialSchema();
		
		return obj;
		
	}
	
	function essentialSchema() {
			var schema = {
	"schema": {
		"columns": {
			"exclude": "INTEGER",
			"og_fullname1": "STRING",
			"og_scanline_name": "STRING",
			"og_fname1": "STRING,REQUIRED",
			"og_lname1": "STRING,REQUIRED",
			"og_fname2": "STRING",
			"og_lname2": "STRING",
			"og_add1": "STRING,REQUIRED",
			"og_add2": "STRING",
			"og_city": "STRING,REQUIRED",
			"og_state": "STRING,REQUIRED",
			"og_zip": "STRING,REQUIRED",
			"og_co": "STRING",
			"og_city_state_zip": "STRING",
			"og_webuser": "STRING",
			"og_email": "STRING",
			"og_webpassword": "STRING",
			"stmt_inv_date": "DATESTRING",
			"stmt_start_date": "DATESTRING",
			"stmt_end_date": "DATESTRING",
			"stmt_bp_desc": "STRING",
			"stmt_curt_bal": "CURRENCY",
			"stmt_amt_due": "CURRENCY",
			"stmt_lt_amt_due": "CURRENCY",
			"stmt_lt_fee": "CURRENCY",
			"stmt_amt_duedate": "DATESTRING",
			"stmt_lt_amt_duedate": "DATESTRING",
			"stmt_futr_chrg_desc": "STRING",
			"stmt_mesg1": "STRING",
			"stmt_mesg2": "STRING",
			"stmt_mesg3": "STRING",
			"stmt_mesg4": "STRING",
			"stmt_beg_bal_date": "DATESTRING",
			"stmt_beg_bal_desc": "STRING",
			"stmt_beg_bal_amt": "CURRENCY",
			"prop_add1": "STRING,REQUIRED",
			"prop_add2": "STRING",
			"md_proc_name1": "STRING",
			"md_proc_name2": "STRING",
			"md_proc_add1": "STRING",
			"md_proc_add2": "STRING",
			"md_proc_city": "STRING",
			"md_proc_state": "STRING",
			"md_proc_zip": "STRING",
			"md_proc_co": "STRING",
			"md_prod_imb": "STRING",
			"md_endors": "STRING",
			"md_rt_add1":"STRING,REQUIRED",
			"md_rt_add2":"STRING,REQUIRED",
			"md_rt_add3":"STRING,REQUIRED",
			"md_rt_add4":"STRING",
			"md_rt_add5":"STRING",
			"hoa_name": "STRING,REQUIRED",
			"hoa_id": "STRING,REQUIRED",
			"prop_acct_number": "STRING,REQUIRED",
			"prop_lot_number": "STRING",
			"prop_record_number": "STRING",
			"bnk_admin_id":"STRING,REQUIRED",
			"bnk_name":"STRING",
			"bnk_add1": "STRING,REQUIRED",
			"bnk_add2": "STRING,REQUIRED",
			"bnk_add3": "STRING",
			"bnk_add4": "STRING",
			"bnk_id": "STRING",
			"bnk_debit":"STRING",
			"bnk_coupon_code":"STRING",
			"stmt_bnk_scanline": "STRING",
			"cb_pmt_freq":"STRING",
			"cb_beg_month":"STRING",
			"cb_beg_year":"STRING",
			"cb_num_Pays":"INTEGER",
			"variable_field_1":"STRING",
			"variable_field_2":"STRING",
			"qr_code":"STRING",
			"ExtraData": "STRING"
		},
		"tables": {
			"stmt_txns": {
				"columns": {
					"index": "STRING",
					"date": "DATESTRING",
					"desc": "STRING",
					"dbt": "CURRENCY",
					"crt": "CURRENCY",
					"bal": "CURRENCY",
					"ExtraData": "STRING"
				}
			},
			"cb_cpns": {
				"columns": {
					"cpn_index":"INTEGER",
					"bnk_scanline": "STRING",
					"cpn_numb":"STRING",
					"date_due": "DATETIME",
					"date_late": "DATETIME",
					"amt_due":"CURRENCY",
					"late_fee":"CURRENCY",
					"ltamt_due":"CURRENCY",
					"mess1":"STRING",
					"mess2":"STRING",
					"line_item1":"STRING",
					"line_item2":"STRING",
					"line_item3":"STRING",
					"line_item4":"STRING",
					"line_item5":"STRING",
					"ExtraData":"STRING"
				}
			}
		}
	}
};
			/*var schema = {
				"schema": {
					"columns": {
						"exclude": "STRING",
						"og_fullname1": "STRING",
						"og_scanline_name": "STRING",
						"og_fname1": "STRING",
						"og_lname1": "STRING",
						"og_fname2": "STRING",
						"og_lname2": "STRING",
						"og_add1": "STRING",
						"og_add2": "STRING",
						"og_city": "STRING",
						"og_state": "STRING",
						"og_zip": "STRING",
						"og_co": "STRING",
						"og_city_state_zip": "STRING",
						"stmt_inv_date": "DATETIME",
						"stmt_start_date": "DATETIME",
						"stmt_end_date": "DATETIME",
						"stmt_bp_desc": "STRING",
						"stmt_curt_bal": "CURRENCY",
						"stmt_amt_due": "CURRENCY",
						"stmt_lt_amt_due": "CURRENCY",
						"stmt_lt_fee": "CURRENCY",
						"stmt_amt_duedate": "DATETIME",
						"stmt_lt_amt_duedate": "DATETIME",
						"stmt_futr_chrg_desc": "STRING",
						"stmt_mesg1": "STRING",
						"stmt_mesg2": "STRING",
						"stmt_mesg3": "STRING",
						"stmt_mesg4": "STRING",
						"stmt_beg_bal_date": "DATETIME",
						"stmt_beg_bal_desc": "STRING",
						"stmt_beg_bal_amt": "CURRENCY",
						"prop_add1": "STRING",
						"prop_add2": "STRING",
						"md_proc_name1": "STRING",
						"md_proc_name2": "STRING",
						"md_proc_add1": "STRING",
						"md_proc_add2": "STRING",
						"md_proc_city": "STRING",
						"md_proc_state": "STRING",
						"md_proc_zip": "STRING",
						"md_proc_co": "STRING",
						"md_proc_city_state_zip": "STRING",
						"md_prod_imb": "STRING",
						"md_endors": "STRING",
						"md_rt_add1":"STRING",
						"md_rt_add2":"STRING",
						"md_rt_add3":"STRING",
						"md_rt_add4":"STRING",
						"md_rt_add5":"STRING",
						"hoa_name": "STRING",
						"hoa_id": "STRING",
						"prop_acct_number": "STRING",
						"bnk_admin_id":"STRING",
						"bnk_name":"STRING",
						"bnk_add1": "STRING",
						"bnk_add2": "STRING",
						"bnk_add3": "STRING",
						"bnk_add4": "STRING",
						"bnk_id": "STRING",
						"stmt_bnk_scanline": "STRING",
						"cb_pmt_freq":"STRING",
						"cb_beg_month":"STRING",
						"cb_beg_year":"STRING",
						"cb_num_Pays":"INTEGER",
						"qr_code":"STRING",
						"ExtraData": "STRING"
					},
					"tables": {
						"stmt_txns": {
							"columns": {
								"index": "STRING",
								"date": "DATETIME",
								"desc": "STRING",
								"dbt": "CURRENCY",
								"crt": "CURRENCY",
								"bal": "CURRENCY",
								"ExtraData": "STRING"
							}
						},
						"cb_cpns": {
							"columns": {
								"cpn_index":"INTEGER",
								"bnk_scanline": "STRING",
								"cpn_numb":"STRING",
								"date_due": "DATETIME",
								"date_late": "DATETIME",
								"amt_due":"CURRENCY",
								"late_fee":"CURRENCY",
								"ltamt_due":"CURRENCY",
								"mess1":"STRING",
								"mess2":"STRING",
								"line_item1":"STRING",
								"line_item2":"STRING",
								"line_item3":"STRING",
								"line_item4":"STRING",
								"line_item5":"STRING",
								"ExtraData":"STRING"
							}
						}
					}
				}
			};
		*/
		return schema;
			
	}
	
}());