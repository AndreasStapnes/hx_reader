
class HX711{
	public:
	void HX711(const int datapin, const int clockpin);
	void ~HX711();


private:
	int datapin;
	int clockpin;
	bool read_bit();
	int32_t read_data();



}
