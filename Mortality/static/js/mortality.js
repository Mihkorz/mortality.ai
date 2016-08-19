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
	
	$("#nnMortalityForm  input[type='number'] ").each(function(){$(this).restrict()});
	
	//BMI calculations
	
	$("#weight_input").change(function(){calculate_bmi()});
	$("#height_input").change(function(){calculate_bmi()});
	
	
	
	
});