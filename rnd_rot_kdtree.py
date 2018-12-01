import numpy as np
from scipy.signal import convolve
from collections import deque

from rptree import rplog
from rptree import Node
from rptree import split_node

def build_rr_kdtree(S, hparams, log=False) :
    logr = lambda message : rplog(message, log)
    
    nrows, ncols = S.shape
    leaf_size = hparams.leaf_size
    logr(
        'Building k-d tree with randomly rotated data '
        'on %i points in %i dims; max. leaf size: %i' 
        % (nrows, ncols, leaf_size)
    )

    # Generate a random rotation matrix
    rotmat = np.random.normal(size=[ncols, ncols])
    # Rotate the input data matrix
    rotated_S = np.dot(S, rotmat)
    
    nodes = deque()
    nidx = 0
    root = Node(0, 0)
    nodes.append((root, root.level, range(nrows)))
    
    while len(nodes) > 0 :
        n, l, idxs = nodes.popleft()
        indent = str('|-') * l;
        logr(
            '%sLevel %i, node %i, %i points ....' 
            % (indent, l, n.idx, len(idxs))
        )
        # choose column equaling level % ncols
        colidx = l % ncols
            
        nidx = split_node(
            hparams.leaf_size,
            rotated_S[:, colidx],
            idxs,
            indent,
            n,
            nidx,
            l + 1,
            nodes,
            logr
        )
    
    return { 'tree' : root, 'rotmat' : rotmat, 'ncols' : ncols }
# -- end function

def traverse_rr_kdtree(tree, log=False) :
    logr = lambda message : rplog(message, log)
    nodes = deque()
    nodes.append(tree['tree'])
    rotmat = np.transpose(tree['rotmat'])
    ncols, _ = rotmat.shape
    print('Rotation matrix:')
    print(rotmat)
    
    while len(nodes) > 0 :
        n = nodes.popleft()
        l = n.level
        indent = str('|-') * l
        ms = ''
        if n.leaf :
            ms = 'pidxs:' + str(n.pidxs)
        else :
            nodes.append(n.lchild)
            nodes.append(n.rchild)
            ms = 'New col:' + str(n.level % ncols) + ', val:' + str(n.val)
        logr(
            '%sL %i: leaf?%i, id:%i --> %s' 
            % (indent, l, n.leaf, n.idx, ms)
        )
# -- end function

def search_rr_kdtree(tree, q) :
    n = tree['tree']
    qprojs = np.dot(q, tree['rotmat'])
    ncols = tree['ncols']
    while not n.leaf :
        if qprojs[n.level % ncols] < n.val :
            n = n.lchild
        else :
            n = n.rchild
    return n.pidxs
# -- end function


def build_rconv_kdtree(S, hparams, log=False) :
    logr = lambda message : rplog(message, log)
    
    nrows, ncols = S.shape
    leaf_size = hparams.leaf_size
    logr(
        'Building k-d tree with randomly convolved data '
        'on %i points in %i dims; max. leaf size: %i' 
        % (nrows, ncols, leaf_size)
    )

    # Generate a random vector for convolution
    rnd_convolve_vector = np.random.normal(size=ncols)
    rcv_preprocess = np.concatenate(
        [ rnd_convolve_vector, rnd_convolve_vector[:-1] ]
    )
    # Convolve the input data matrix
    rconvolved_S = np.array([
        convolve(p, rcv_preprocess, 'valid', method='auto') for p in S
    ])

    a, b = rconvolved_S.shape
    assert a == nrows and b == ncols
    
    nodes = deque()
    nidx = 0
    root = Node(0, 0)
    nodes.append((root, root.level, range(nrows)))
    
    while len(nodes) > 0 :
        n, l, idxs = nodes.popleft()
        indent = str('|-') * l;
        logr(
            '%sLevel %i, node %i, %i points ....' 
            % (indent, l, n.idx, len(idxs))
        )
        # choose column equaling level % ncols
        colidx = l % ncols
            
        nidx = split_node(
            hparams.leaf_size,
            rconvolved_S[:, colidx],
            idxs,
            indent,
            n,
            nidx,
            l + 1,
            nodes,
            logr
        )
    
    return {
        'tree' : root,
        'rnd_vec' : rnd_convolve_vector,
        'conv_vec' : rcv_preprocess,
        'ncols' : ncols
    }
# -- end function


def traverse_rconv_kdtree(tree, log=False) :
    logr = lambda message : rplog(message, log)
    nodes = deque()
    nodes.append(tree['tree'])
    print('Random convoolution vector:', tree['rnd_vec'])
    ncols = tree['ncols']
    
    while len(nodes) > 0 :
        n = nodes.popleft()
        l = n.level
        indent = str('|-') * l
        ms = ''
        if n.leaf :
            ms = 'pidxs:' + str(n.pidxs)
        else :
            nodes.append(n.lchild)
            nodes.append(n.rchild)
            ms = 'New col:' + str(n.level % ncols) + ', val:' + str(n.val)
        logr(
            '%sL %i: leaf?%i, id:%i --> %s' 
            % (indent, l, n.leaf, n.idx, ms)
        )
# -- end function


def search_rconv_kdtree(tree, q) :
    n = tree['tree']
    qprojs = convolve(q, tree['conv_vec'], 'valid', method='auto')
    assert len(qprojs) == tree['ncols']
    ncols = tree['ncols']
    while not n.leaf :
        if qprojs[n.level % ncols] < n.val :
            n = n.lchild
        else :
            n = n.rchild
    return n.pidxs
# -- end function