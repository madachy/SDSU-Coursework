package data_structures;

import java.util.ConcurrentModificationException;
import java.util.Iterator;

/**
 * William Fox cssc0917
 * prog3 HashTable.java
 */
public class HashTable<K extends Comparable<K>, V> implements DictionaryADT<K, V> {

    private UnorderedList<DictionaryNode<K, V>>[] list;
    private int currentSize, maxSize, tableSize;
    private long modificationCounter;

    public HashTable(int size) {
        maxSize = size;
        tableSize = (int) (maxSize * 1.3);
        modificationCounter = currentSize = 0;
        list = new UnorderedList[tableSize];
        for (int i = 0; i < tableSize; i++)
            list[i] = new UnorderedList<DictionaryNode<K, V>>();
    }

    /**
     * Returns true if the dictionary has an object identified by
     * key in it, otherwise false.
     *
     * @param key
     */
    public boolean contains(K key) {
        return list[getIndex(key)].contains(new DictionaryNode<K, V>(key, null));
    }

    /**
     * Adds the given key/value pair to the dictionary.  Returns
     * false if the dictionary is full, or if the key is a duplicate.
     * Returns true if addition succeeded.
     *
     * @param key
     * @param value
     */
    public boolean add(K key, V value) {
        if (isFull()) return false;
        int index = getIndex(key);
        DictionaryNode<K, V> tmp = new DictionaryNode(key, value);
        //DictionaryNode<K, V> returnValue = list[index].find(tmp);
        boolean returnValue = list[index].contains(tmp);
        if (returnValue)    //Key already present
            return false;
        list[index].addLast(tmp);
        currentSize++;
        modificationCounter++;
        return true;
    }

    /**
     * Deletes the key/value pair identified by the key parameter.
     * Returns true if the key/value pair was found and removed, otherwise false.
     *
     * @param key
     */
    public boolean delete(K key) {
        boolean bool = list[getIndex(key)].remove(new DictionaryNode<K, V>(key, null));
        currentSize--;
        modificationCounter++;
        return bool;
    }

    /**
     * Returns the value associated with the parameter key.  Returns
     * null if the key is not found or the dictionary is empty.
     *
     * @param key
     */
    public V getValue(K key) {
        if (isEmpty()) return null;
        int index = getIndex(key);
        DictionaryNode<K, V> returnValue = list[index].find(new DictionaryNode(key, null));
        if (returnValue == null) //Not Found
            return null;
        return returnValue.value;
    }

    /**
     * Returns the key associated with the parameter value.  Returns
     * null if the value is not found in the dictionary.  If more
     * than one key exists that matches the given value, returns the
     * first one found.
     *
     * @param value
     */
    public K getKey(V value) {
        for (int i = 0; i < tableSize; i++)
            for (DictionaryNode<K, V> dn : list[i])
                if (((Comparable<V>) dn.value).compareTo(value) == 0)
                    return dn.key;
        return null;
    }

    /**
     * Returns the number of key/value pairs currently stored
     * in the dictionary
     */
    public int size() {
        return currentSize;
    }

    /**
     * Returns true if the dictionary is at max capacity
     */
    public boolean isFull() {
        return currentSize == maxSize;
    }

    /**
     * Returns true if the dictionary is empty
     */
    public boolean isEmpty() {
        return currentSize == 0;
    }

    /**
     * Returns the Dictionary object to an empty state.
     */
    public void clear() {
        for (int i = 0; i < tableSize; i++) {
            list[i].clear();
        }
        currentSize = 0;
        modificationCounter = 0;
    }

    private int getIndex(K key) {
        int index = key.hashCode();
        index = index & 0x7FFFFFFF; //abs(index)
        index %= maxSize;
        return index;
    }


    //~~~~~~~~~~~~~~~~~~~~~Iterators and DictionaryNode Classes Below~~~~~~~~~~~~~~~~~~~~~~~~
    abstract class IteratorHelper<E> implements Iterator<E> {
        protected DictionaryNode<K, V>[] nodes;
        protected int index;
        protected long modificationCheck;

        public IteratorHelper() {
            nodes = new DictionaryNode[currentSize];
            int j = 0;
            for (int i = 0; i < tableSize; i++)
                for (DictionaryNode dn : list[i]) //Loads array w/ all Dn's
                 nodes[j++] = dn;
            nodes = shellSort(nodes);
            index = 0;
            modificationCheck = modificationCounter;
        }

        private DictionaryNode[] shellSort(DictionaryNode[] list) {
            DictionaryNode<K, V> temp;
            int in, out, h = 1;
            int size = list.length;

            while (h <= size / 3)
                h = h * 3 + 1;
            while (h > 0) {
                for (out = h; out < size; out++) {
                    temp = list[out];
                    in = out;
                    while (in > h - 1 && list[in - h].compareTo(temp) >= 0) {
                        list[in] = list[in - h];
                        in -= h;
                    }
                    list[in] = temp;
                } //for
                h = (h - 1) / 3;
            }//while
            return list;
        }//shellSort

        public boolean hasNext() {
            if (modificationCheck != modificationCounter)
                throw new ConcurrentModificationException();
            return index < currentSize;
        }

        public abstract E next();

        public void remove() {
            throw new UnsupportedOperationException();
        }

    }//IteratorHelper

    class KeyIteratorHelper extends IteratorHelper<K> {
        public KeyIteratorHelper() {
            super();
        }

        public K next() {
            return nodes[index++].key;
        }
    }//KeyIteratorHelper

    class ValueIteratorHelper extends IteratorHelper<V> {
        public ValueIteratorHelper() {
            super();
        }

        public V next() {
            return nodes[index++].value;
        }
    }//ValueIteratorHelper

    /**
     * Returns an Iterator of the keys in the dictionary, in ascending
     * sorted order.  The iterator must be fail-fast.
     */
    public Iterator keys() {
        return new KeyIteratorHelper();
    }


    /**
     * Returns an Iterator of the values in the dictionary.  The
     * order of the values must match the order of the keys.
     * The iterator must be fail-fast.
     */
    public Iterator values() {
        return new ValueIteratorHelper();
    }

    private class DictionaryNode<K extends Comparable<K>, V> implements Comparable<DictionaryNode<K, V>> {
        K key;
        V value;

        public DictionaryNode(K k, V v) {
            key = k;
            value = v;
        }

        public int compareTo(DictionaryNode<K, V> node) {
            return key.compareTo(node.key);
        }
    }//Dictionary Node


}//Eof