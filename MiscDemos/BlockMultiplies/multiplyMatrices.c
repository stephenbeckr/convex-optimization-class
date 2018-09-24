#if defined(__GNUC__) && !(defined(__clang__)) && defined(NEEDS_UCHAR)
#include <uchar.h>
#endif
#include <math.h>
#include "mex.h"


void mexFunction( int nlhs, mxArray *plhs[], 
		  int nrhs, const mxArray*prhs[] ) 
{ 
    double *A, *B, *C;
    mwSize m, n, k;
    mwIndex i, j, u;
    
    if ( nrhs != 2 ) {
        mexPrintf("Usage:  C = multiplyMatrices(A,B)\n");
        mexErrMsgIdAndTxt("MATLAB:mexFile:invlaidNumInputs","Need 2 inputs");
    }
    
    A   = mxGetPr( prhs[0] ); /* A is m x k */
    m   = mxGetM(  prhs[0] );
    k   = mxGetN(  prhs[0] );
    
    B   = mxGetPr( prhs[1] ); /* A is m x k */
    if (k != mxGetM(  prhs[1] ) ){
        mexPrintf("Usage:  C = multiplyMatrices(A,B), where size(A,2)==size(B,1)\n");
        mexErrMsgIdAndTxt("MATLAB:mexFile:invlaidNumInputs","Wrong size");
    }
    n   = mxGetN(  prhs[1] );
    
    plhs[0] = mxCreateDoubleMatrix( m, n, mxREAL );
    C       = mxGetPr( plhs[0] );
    
    
    /* Now, the actual computation */
    for (i=0; i<m; i++)
        for (j=0;j<n;j++)
            for (u=0;u<k;u++)
                C[i+m*j] += A[i+m*u]*B[u+j*k];
}