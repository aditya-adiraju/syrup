FROM aflplusplus/aflplusplus

RUN apt update && apt install -y \
    python3\
    python3-pip 

# shellphish_qemu and shellphish_afl
RUN git clone https://github.com/angr/wheels.git\
    && pip3 install wheels/shellphish*.whl

# driller
RUN git clone https://github.com/shellphish/driller.git \
    && pip3 install -r driller/requirements.txt \
    && pip3 install -e driller 

# rex, tracer is already installed from driller
# RUN git clone https://github.com/angr/rex.git \
#     # && pip install -r rex/requirements.txt \
#     && pip install angr angrop keystone-engine \
#     && pip install -e rex