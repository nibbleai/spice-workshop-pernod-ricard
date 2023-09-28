from setuptools import setup

if __name__ == "__main__":
   setup(
      name="NYC Taxi - spice demo",
      version="1.0",
      description="An example project to demo spice.",
      author="nibble",
      author_email="contact@nibble.ai",
      packages=["src"],
      install_requires=[
         "pandas==2.0.3",
         "scikit-learn==1.0.2",
         "spice[full]==2023.07.04",
         "httpx",
         "ydata-profiling",
         "matplotlib==3.7.0",
         "jupyter",
      ]
   )
