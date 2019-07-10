SCRIPT_DIR=`dirname $0`
BUILD_DIR="build/"

HIER_BLOCK_DIR="$SCRIPT_DIR/grc/hier"
MOD_BLOCK_DIR="$SCRIPT_DIR/grc/modulations"

CMD=$1

case $CMD in
    build)
        echo "Building Hierarchical Blocks -> ~/.grc_gnuradio"
        for f in $HIER_BLOCK_DIR/*.grc;
        do 
        echo "Building $f ..."; 
        grcc $f
        done
        
        echo "Building Modulation Blocks -> ~/.grc_gnuradio"
        for f in $MOD_BLOCK_DIR/*.grc;
        do 
        echo "Building $f ..."; 
        grcc $f
        done
        ;;
    test)
        echo "Testing"
        cd $SCRIPT_DIR
        python -m tests
        ;;
    *)
        echo "
        Available Commands
        ------------------
        test
        "
        ;;
esac