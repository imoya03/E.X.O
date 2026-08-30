#define EMG_PIN A0
#define SAMPLE_RATE_HZ 1000
#define START_BYTE 0xAA

volatile bool sampleReady = false;

void setupTimer() {
  noInterrupts();
  TCCR1A = 0;
  TCCR1B = 0;
  TCNT1 = 0;

  TCCR1B |= (1 << WGM12);              // CTC mode
  TCCR1B |= (1 << CS11) | (1 << CS10); // prescaler 64
  OCR1A = (16000000UL / 64 / SAMPLE_RATE_HZ) - 1; // 249 para 1000Hz
  TIMSK1 |= (1 << OCIE1A);

  interrupts();
}

ISR(TIMER1_COMPA_vect) {
  sampleReady = true;
}

void setup() {
  Serial.begin(115200);
  setupTimer();
}

void loop() {
  if (sampleReady) {
    sampleReady = false;

    uint16_t value = analogRead(EMG_PIN); // 0-1023

    uint8_t highByte = (value >> 8) & 0xFF;
    uint8_t lowByte  = value & 0xFF;
    uint8_t checksum = highByte ^ lowByte;

    Serial.write(START_BYTE);
    Serial.write(highByte);
    Serial.write(lowByte);
    Serial.write(checksum);
  }
}