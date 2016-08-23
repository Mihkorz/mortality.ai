(function ($) {
    $.fn.restrict = function () {
        // returns the collection returned by the selector, over which we iterate:
        return this.each(function(){
            // binding a change event-handler:
        	if ($(this).attr("name")!='height' && $(this).attr("name")!='weight' ){
            $(this).on('change', function(){
                // caching the 'this' (the current 'input'):
                var _self = this,
                    // creating numbers from the entered-value,
                    // the min and the max:
                    v = parseFloat(_self.value),
                    min = parseFloat(_self.min),
                    max = parseFloat(_self.max);
                // if it's in the range we leave the value alone (or set
                // it back to the entered value):
                if (v >= min && v <= max){
                    _self.value = v;
                }
                else {
                    // otherwise we test to see if it's less than the min,
                    // if it is we reset the value to the min, otherwise we reset
                    // to the max:
                    _self.value = v < min ? min : max;
                }
            });
          }// end of if not weight height smoke
        });
    };
})(jQuery);

function calculate_bmi(){
	$("#bmi_rate").text();
	weight = $("#weight_input").val();
	height = $("#height_input").val();
	if(!height) bmi=0;
	if(!weight) bmi=0;
	
	if(weight && height) bmi = (weight/(height*height))*10000;
	
	
	
	$("#bmi_rate").text(Math.round(bmi).toFixed(2));
	
}

$(function () { 
	
	// substitute with min\max values if input value exceeds them
	$("#nnMortalityForm  input[type='number'] ").each(function(){$(this).restrict()});
	
	// BMI calculations	
	$("#weight_input").keyup(function(){calculate_bmi()});
	$("#height_input").keyup(function(){calculate_bmi()});
	
	// substitude alcohol buttons basing on chosen gender
	$('#sex_selector label.btn').click(function() {
	    $(this).addClass('active').siblings().removeClass('active');
	    
	    var sex = $(this).find("input").val();
	    
	    if (sex==0){ 
	    	$("#alcohol_select").html('<label class="btn btn-success"> \
	                <input type="radio" name="alcohol" id="alcohol0" autocomplete="off" value="0" required> Non-drinker \
	              </label> \
	              <label class="btn btn-success"> \
	                <input type="radio" name="alcohol" id="alcohol1" autocomplete="off" value="1" required> < 1 drink/month \
	              </label> \
	              <label class="btn btn-success"> \
	                <input type="radio" name="alcohol" id="alcohol2" autocomplete="off" value="2" required> 0-2 drinks/week \
	              </label> \
	              <label class="btn btn-success"> \
	                <input type="radio" name="alcohol" id="alcohol3" autocomplete="off" value="3" required> 3-5 drinks/week \
	              </label> \
	              <label class="btn btn-success"> \
	                <input type="radio" name="alcohol" id="alcohol4" autocomplete="off" value="4" required> 6-17 drinks/week &nbsp; \
	              </label> \
	              <label class="btn btn-success"> \
	                <input type="radio" name="alcohol" id="alcohol5" autocomplete="off" value="5" required> Heavy drinker \
	              </label>');
	    }
	    else{
	    	$("#alcohol_select").html('<label class="btn btn-success"> \
              <input type="radio" name="alcohol" id="alcohol0" autocomplete="off" value="0" required> Non-drinker \
            </label> \
            <label class="btn btn-success"> \
              <input type="radio" name="alcohol" id="alcohol1" autocomplete="off" value="1" required> < 1 drink/month \
            </label> \
            <label class="btn btn-success"> \
              <input type="radio" name="alcohol" id="alcohol2" autocomplete="off" value="2" required> 0-4 drinks/week \
            </label> \
            <label class="btn btn-success"> \
              <input type="radio" name="alcohol" id="alcohol3" autocomplete="off" value="3" required> 5-9 drinks/week \
            </label> \
            <label class="btn btn-success"> \
              <input type="radio" name="alcohol" id="alcohol4" autocomplete="off" value="4" required> 10-24 drinks/week \
            </label> \
            <label class="btn btn-success"> \
              <input type="radio" name="alcohol" id="alcohol5" autocomplete="off" value="5" required> Heavy drinker \
            </label>');
	    }
	    

	    // TODO: insert whatever you want to do with $(this) here
	});
	
	
	$("#submitBtn").click(function(){
		if($("#nnMortalityForm").valid()) {
		    $("#pathmodal").modal("show");
		}
	});	
	
});