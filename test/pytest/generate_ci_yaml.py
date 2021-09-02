import yaml
import glob

base = """
.pytest:
  image: gitlab-registry.cern.ch/fastmachinelearning/hls4ml-testing:0.1.base
  tags: 
    - docker
  before_script:
    - source ~/.bashrc
    - git submodule init
    - git submodule update
    - conda activate hls4ml-testing
    - pip install .[profiling]
  script:
    - cd test/pytest
    - pytest $PYTESTFILE -rA --cov-report xml --cov-report term --cov=hls4ml --junitxml=report.xml
  artifacts:
    when: always
    reports:
      junit: 
        - test/pytest/report.xml
      cobertura:
        - test/pytest/coverage.xml
    paths:
      - test/pytest/hls4mlprj*.tar.gz
"""

template = """
pytest.{}:
  extends: .pytest
  variables:
    PYTESTFILE: {} 
"""

yml = yaml.safe_load(base)
tests = glob.glob('test_*.py')
for test in tests:
    name = test.replace('test_','').replace('.py','')
    yml.update(yaml.safe_load(template.format(name, 'test_{}.py'.format(name))))

yamlfile = open('pytests.yml', 'w')
yaml.safe_dump(yml, yamlfile)