## Solving multi-dimensional minimization problems with restrictions
- [Solving multi-dimensional minimization problems with restrictions](#solving-multi-dimensional-minimization-problems-with-restrictions)
  - [Description](#description)
  - [Get started](#get-started)
  - [Project structure](#project-structure)
  - [Results](#results)


### Description
    f(x) = 4x_1+x_2+4*sqrt(1+3x_1^2+x_2^2)
     1. Найти minf(x) на заданном отрезке с точностью [0.1, 0.01, 0.001] с помощью трех методов: метода равномерного поиска, метода пробных точек  и метода золотого сечения 
     2. Сравнить методы. В качестве критерия использовать число обращений к вычислению функции
     3. Сравнить методы с теоретическими оценками

### Get started
```bash
git clone https://github.com/IMZolin/one-dimension-minimization <your project name>
cd <your project name>
pip install -r requirements.txt
```

### Project structure
```bash
├───graphics            # images:graphics+scheme of simplex
├───report
│   └───lab3_opt_methods.pdf 
├───src                 # code
│   ├───golden_egg.py      # Golden Ratio Method
│   ├───main.py  # corner dots 
│   ├───One_D_Problem_file.py # one dimension minimization problem class
│   ├───result_analisys.py  # get results
│   ├───test_uniform.py # test code for running uniform search method
│   ├───result_analisys.py # get results
│   ├───Trial_Point_Method_file.py # Trial Point Method
└───────uniform_search.py # Uniform Search Method
```

### Results
1. Golden Ratio Method
<img src="images/2-gold.png" alt="golden ratio method">
2. Trial Point Method
<img src="images/2-tpm.png" alt="trial point method">
3. Uniform Search Method
<img src="images/2-us.png" alt="uniform search method">
4. Comparison of methods
<img src="images/2-compare.png" alt="comparison of methods">
