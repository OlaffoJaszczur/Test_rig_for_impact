#include <stdio.h>
#include <stdbool.h>

#include "main.h"
#include "stm_init.c"
#include "logic.c"

#define SERVO_PWM_PIN GPIO_PIN_6
#define SERVO_GPIO_PORT GPIOA
#define LOAD_CELL_ADC_CHANNEL ADC_CHANNEL_1
#define PHOTOCELL_PIN GPIO_PIN_1
#define PHOTOCELL_PORT GPIOB

UART_HandleTypeDef huart2;

volatile bool user_input_ready = false;
volatile bool impactor_ready = false;
volatile bool drop_ready = false;
float predefined_mass = 1.0;
float desired_force = 0.0;
float drop_height = 0.0;

int main(void)
{
  HAL_Init();
  SystemClock_Config();
  MX_GPIO_Init();
  MX_USART2_UART_Init();

  while (1) 
  {
    if (user_input_ready) 
    {
        drop_height = desired_force / (predefined_mass * 9.81);

        uint16_t servo_angle = (uint16_t)(drop_height * 10);

        Servo_SetAngle(servo_angle);

        impactor_ready = true;
        user_input_ready = false;
    }

    if (impactor_ready && drop_ready) 
    {
        Start_Data_Recording();

        Servo_SetAngle(0);

        HAL_Delay(2000);

        Stop_Data_Recording();
        Plot_Data();

        if (/* User chooses to export data */) 
        {
            Export_Data_To_CSV();
        }

        drop_ready = false;
        impactor_ready = false;
    }
  }
}
