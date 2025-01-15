#include "main.h"
#include <stdbool.h>

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

void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_USART2_UART_Init(void);

int main(void)
{
  HAL_Init();
  SystemClock_Config();
  MX_GPIO_Init();
  MX_USART2_UART_Init();

  while (1)
  {
    if(serialConnection)
      {
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

                drop_ready = false;
                impactor_ready = false;
            }
          }
      }
  }
}

void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_NONE;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }

  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_HSI;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_0) != HAL_OK)
  {
    Error_Handler();
  }
}

static void MX_USART2_UART_Init(void)
{
  huart2.Instance = USART2;
  huart2.Init.BaudRate = 38400;
  huart2.Init.WordLength = UART_WORDLENGTH_8B;
  huart2.Init.StopBits = UART_STOPBITS_1;
  huart2.Init.Parity = UART_PARITY_NONE;
  huart2.Init.Mode = UART_MODE_TX_RX;
  huart2.Init.HwFlowCtl = UART_HWCONTROL_NONE;
  huart2.Init.OverSampling = UART_OVERSAMPLING_16;
  huart2.Init.OneBitSampling = UART_ONE_BIT_SAMPLE_DISABLE;
  huart2.AdvancedInit.AdvFeatureInit = UART_ADVFEATURE_NO_INIT;
  if (HAL_UART_Init(&huart2) != HAL_OK)
  {
    Error_Handler();
  }
}

static void MX_GPIO_Init(void)
{
  __HAL_RCC_GPIOF_CLK_ENABLE();
  __HAL_RCC_GPIOA_CLK_ENABLE();
}

bool serialConnection(void)
{
    // Get connection with GUI
}

void SystemClock_Config(void) {
    // Configure the system clock (placeholder, adjust as needed)
}

void GPIO_Init(void) {
    // Initialize GPIO for servo, photocell, etc.
}

void ADC_Init(void) {
    // Initialize ADC for load cell
}

void TIM_PWM_Init(void) {
    // Initialize PWM timer for servo control
}

void UART_Init(void) {
    // Initialize UART for user communication
}

void setStepper(uint16_t angle) {
    // Set servo position based on angle
}

void Start_Data_Recording(void) {
    // Start recording data from sensors
}

void Stop_Data_Recording(void) {
    // Stop recording data from sensors
}

void Error_Handler(void)
{
  __disable_irq();
  while (1)
  {
  }
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */
